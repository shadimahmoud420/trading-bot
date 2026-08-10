#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 XAUUSD (الذهب) Trading Analysis Bot
Telegram Bot for Gold Technical Analysis
مع دمج متقدم للمؤشرات الفنية وإدارة رأس المال

بناء بواسطة: شادي محمود
الهدف: توصيات ذهب دقيقة عالية الجودة
"""

import asyncio
import logging
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import yfinance as yf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import *
from indicators import TechnicalIndicators, MoneyManagement

# 🔧 إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoldTradingBot:
    """البوت الرئيسي لتحليل الذهب"""
    
    def __init__(self):
        self.chat_ids = set()  # مجموعة معرّفات الدردشات
        self.last_signal = {}  # آخر إشارة تم إرسالها
        self.db_file = "signals.db"
        self.setup_database()
    
    def setup_database(self):
        """إعداد قاعدة بيانات SQLite"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                timeframe TEXT,
                signal TEXT,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                indicators_json TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER UNIQUE,
                joined_date DATETIME
            )
        """)
        conn.commit()
        conn.close()
    
    def add_user(self, chat_id: int):
        """إضافة مستخدم جديد"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (chat_id, joined_date) VALUES (?, ?)",
                (chat_id, datetime.now())
            )
            conn.commit()
            conn.close()
            self.chat_ids.add(chat_id)
            logger.info(f"✅ مستخدم جديد: {chat_id}")
        except Exception as e:
            logger.error(f"❌ خطأ في إضافة المستخدم: {e}")
    
    def save_signal(self, timeframe: str, signal: Dict):
        """حفظ الإشارة في قاعدة البيانات"""
        if not STORE_SIGNALS:
            return
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO signals 
                (timestamp, timeframe, signal, entry_price, stop_loss, take_profit, indicators_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now(),
                timeframe,
                signal.get("signal_type"),
                signal.get("entry"),
                signal.get("stop_loss"),
                signal.get("take_profit"),
                json.dumps(signal.get("indicators", {}))
            ))
            conn.commit()
            conn.close()
            logger.info(f"💾 تم حفظ الإشارة: {timeframe} - {signal.get('signal_type')}")
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ الإشارة: {e}")
    
    async def fetch_data(self, timeframe: str, periods: int = 100) -> Optional[pd.DataFrame]:
        """جلب بيانات الذهب من yfinance"""
        try:
            # تحويل الفريم إلى صيغة yfinance
            interval_map = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h"}
            interval = interval_map.get(timeframe, "1m")
            
            # تحميل البيانات
            data = yf.download(
                "XAUUSD=X",
                period="7d",
                interval=interval,
                progress=False
            )
            
            if data is None or len(data) == 0:
                logger.error(f"❌ لم يتم الحصول على بيانات للفريم {timeframe}")
                return None
            
            return data[-periods:]
        
        except Exception as e:
            logger.error(f"❌ خطأ في جلب البيانات: {e}")
            return None
    
    def generate_signal(self, analysis: Dict) -> Optional[Dict]:
        """توليد إشارة من تحليل المؤشرات"""
        
        signals = analysis.get("signals", {})
        
        # عد الإشارات
        buy_signals = sum(1 for s in signals.values() if "BUY" in str(s))
        sell_signals = sum(1 for s in signals.values() if "SELL" in str(s))
        total_signals = len(signals)
        
        if total_signals == 0:
            return None
        
        buy_ratio = buy_signals / total_signals
        sell_ratio = sell_signals / total_signals
        
        # اتخاذ قرار الإشارة
        if buy_ratio >= SIGNAL_THRESHOLD:
            signal_type = "BUY"
            confidence = buy_ratio
        elif sell_ratio >= SIGNAL_THRESHOLD:
            signal_type = "SELL"
            confidence = sell_ratio
        else:
            return None
        
        # حساب TP و SL
        current_price = analysis["current_price"]
        tp_sl = MoneyManagement.calculate_tp_sl(current_price, signal_type)
        
        if tp_sl is None:
            return None
        
        return {
            "signal_type": signal_type,
            "confidence": confidence,
            "entry": current_price,
            "stop_loss": tp_sl["stop_loss"],
            "take_profit": tp_sl["take_profit"],
            "risk_reward": tp_sl["risk_reward_ratio"],
            "indicators": analysis["indicators"],
            "signals_breakdown": signals,
            "timestamp": analysis["timestamp"]
        }
    
    def format_signal_message(self, timeframe: str, signal: Dict, 
                             account_balance: float = 250) -> str:
        """تنسيق رسالة الإشارة"""
        
        # حساب حجم العقد
        mm = MoneyManagement.calculate_position_size(
            account_balance,
            RISK_PERCENTAGE,
            signal["entry"],
            signal["stop_loss"]
        )
        
        # بناء الرسالة بالعربية (Palestinian Arabic)
        emoji_signal = "🟢 شراء" if signal["signal_type"] == "BUY" else "🔴 بيع"
        
        message = f"""
╔════════════════════════════════════╗
║   🤖 إشارة تحليل الذهب (XAUUSD)   ║
╚════════════════════════════════════╝

{emoji_signal}
───────────────────────────────
⏱️ الفريم الزمني: {timeframe}
🎯 نسبة التأكيد: {signal['confidence']*100:.1f}%
📊 السعر الحالي: ${signal['entry']:.2f}

📈 نقاط التداول:
├─ نقطة الدخول: ${signal['entry']:.2f}
├─ وقف الخسارة: ${signal['stop_loss']:.2f}
└─ الهدف: ${signal['take_profit']:.2f}

💰 إدارة رأس المال:
├─ الحساب: ${account_balance:.2f}
├─ نسبة المخاطرة: {RISK_PERCENTAGE*100}%
├─ قيمة المخاطرة: ${mm['risk_amount']:.2f}
├─ حجم العقد: {mm['position_size']:.4f}
└─ Risk/Reward: 1:{signal['risk_reward']:.2f}

🔍 المؤشرات الفنية:
"""
        
        # إضافة تفاصيل المؤشرات
        indicators = signal.get("indicators", {})
        if indicators.get("RSI"):
            message += f"├─ RSI: {indicators['RSI']:.2f} {signal['signals_breakdown'].get('RSI', 'N/A')}\n"
        if indicators.get("MACD"):
            message += f"├─ MACD: {indicators['MACD']:.6f} {signal['signals_breakdown'].get('MACD', 'N/A')}\n"
        if indicators.get("EMA_20"):
            message += f"├─ EMA20: ${indicators['EMA_20']:.2f}\n"
        if indicators.get("EMA_50"):
            message += f"├─ EMA50: ${indicators['EMA_50']:.2f}\n"
        if indicators.get("Stochastic_K"):
            message += f"└─ Stochastic: {indicators['Stochastic_K']:.2f}\n"
        
        message += f"""
⏰ الوقت: {signal['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
───────────────────────────────

⚠️ إخلاء المسؤولية:
هذه الإشارات لأغراض تعليمية فقط
لا تشكل نصيحة مالية
تاجر بحذر وحسب إدارة المخاطر الخاصة بك

#XAUUSD #ذهب #تحليل_فني #إشارات_تداول
"""
        return message
    
    async def analyze_and_broadcast(self, context: ContextTypes.DEFAULT_TYPE):
        """تحليل وبث الإشارات"""
        logger.info("🔄 بدء التحليل الدوري...")
        
        for timeframe in TIMEFRAMES:
            try:
                # جلب البيانات
                data = await self.fetch_data(timeframe, periods=100)
                if data is None:
                    continue
                
                # حساب المؤشرات
                prices = data['Close'].values
                highs = data['High'].values
                lows = data['Low'].values
                
                analysis = TechnicalIndicators.analyze_all_indicators(
                    prices, highs, lows
                )
                
                # توليد الإشارة
                signal = self.generate_signal(analysis)
                
                if signal is None:
                    logger.info(f"ℹ️ لا توجد إشارة قوية للفريم {timeframe}")
                    continue
                
                # التحقق من تكرار الإشارة
                signal_key = f"{timeframe}_{signal['signal_type']}"
                last_signal_time = self.last_signal.get(signal_key)
                
                if last_signal_time and (datetime.now() - last_signal_time).seconds < 3600:
                    logger.info(f"⏭️ تجاهل إشارة متكررة: {signal_key}")
                    continue
                
                # حفظ الإشارة
                self.save_signal(timeframe, signal)
                self.last_signal[signal_key] = datetime.now()
                
                # بث الإشارة
                message = self.format_signal_message(timeframe, signal)
                
                for chat_id in self.chat_ids:
                    try:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=message,
                            parse_mode="HTML"
                        )
                        logger.info(f"✅ تم إرسال الإشارة إلى {chat_id}")
                    except Exception as e:
                        logger.error(f"❌ خطأ في الإرسال للمستخدم {chat_id}: {e}")
            
            except Exception as e:
                logger.error(f"❌ خطأ في التحليل للفريم {timeframe}: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    chat_id = update.effective_chat.id
    bot.add_user(chat_id)
    
    welcome_message = """
╔════════════════════════════════════╗
║  🤖 مرحباً في بوت تحليل الذهب     ║
║   XAUUSD Trading Analysis Bot      ║
╚════════════════════════════════════╝

🎯 الميزات:
✅ تحليل فني متقدم للذهب
✅ دمج 5 مؤشرات (RSI, MACD, Bollinger, EMA, Stochastic)
✅ فريمات 1 و 5 دقائق
✅ إدارة رأس مال احترافية (3% مخاطرة)
✅ توصيات BUY/SELL دقيقة
✅ إشعارات فورية للإشارات الجديدة

📊 الأوامر المتاحة:
/start - بدء البوت
/status - حالة البوت
/latest - آخر إشارة
/balance - حساب رأس المال
/help - المساعدة

⚠️ إخلاء المسؤولية:
هذه الإشارات لأغراض تعليمية فقط
لا تشكل نصيحة مالية

تم بناؤه بواسطة: شادي محمود 🇵🇸
"""
    await update.message.reply_text(welcome_message)
    logger.info(f"✅ انضم المستخدم: {chat_id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help"""
    help_text = """
📚 دليل الاستخدام:

🎯 الأوامر الأساسية:
/start - البدء
/status - حالة البوت الحالية
/latest - آخر إشارة تم إرسالها
/stats - إحصائيات الإشارات

💰 إدارة رأس المال:
/balance <amount> - تعيين رصيد الحساب

📊 المؤشرات المستخدمة:
1️⃣ RSI - مؤشر القوة النسبية
2️⃣ MACD - التقارب والتباعد
3️⃣ Bollinger Bands - العصابات
4️⃣ EMA - المتوسطات المتحركة
5️⃣ Stochastic - مؤشر ستوكاستيك

⏱️ الفريمات:
• 1 دقيقة (1m)
• 5 دقائق (5m)

💡 النصائح:
• تابع الإشارات بانتظام
• استخدم إدارة رأس المال
• تاجر برصيد معقول

📞 للمساعدة: @shadimahmoud
"""
    await update.message.reply_text(help_text)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /status"""
    status_message = f"""
🟢 البوت يعمل بشكل طبيعي ✅

📊 الإحصائيات:
├─ عدد المستخدمين: {len(bot.chat_ids)}
├─ الفريمات المراقبة: {', '.join(TIMEFRAMES)}
├─ نسبة التأكيد المطلوبة: {SIGNAL_THRESHOLD*100}%
└─ نسبة المخاطرة: {RISK_PERCENTAGE*100}%

🕐 معلومات النظام:
├─ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
├─ الرمز: {SYMBOL}
└─ الحالة: متصل ✅

⚙️ الإعدادات:
├─ رصيد الحساب: ${ACCOUNT_BALANCE_MIN}-${ACCOUNT_BALANCE_MAX}
├─ تحديث كل: {UPDATE_INTERVAL} ثانية
└─ وضع التصحيح: {'مفعّل' if DEBUG_MODE else 'معطّل'}
"""
    await update.message.reply_text(status_message)

async def main():
    """الدالة الرئيسية"""
    global bot
    bot = GoldTradingBot()
    
    # إنشاء التطبيق
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    
    # إضافة مهمة دورية للتحليل
    application.job_queue.run_repeating(
        bot.analyze_and_broadcast,
        interval=UPDATE_INTERVAL,
        first=10
    )
    
    logger.info("🚀 تم بدء البوت...")
    
    # بدء البوت
    async with application:
        await application.start()
        logger.info("✅ البوت يعمل الآن!")
        await application.updater.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ تم إيقاف البوت")
    except Exception as e:
        logger.error(f"❌ خطأ فادح: {e}")
