#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    BOT_TOKEN = "8757189559:AAFw0VLGnEwKBtxqIWwTouB9nJxz6IBPXn0"

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"🤖 مرحباً {user.first_name}!\n\n"
        "╔════════════════════════════════════╗\n"
        "║   🤖 بوت تحليل الذهب (XAUUSD)     ║\n"
        "║   Gold Trading Analysis Bot        ║\n"
        "╚════════════════════════════════════╝\n\n"
        "✅ التحليل الفني المتقدم\n"
        "✅ دمج 5 مؤشرات فنية\n"
        "✅ إدارة رأس المال احترافية\n"
        "✅ توصيات عالية الجودة\n\n"
        "📚 الأوامر المتاحة:\n"
        "/help - المساعدة\n"
        "/status - حالة البوت\n"
        "/balance - الحساب\n\n"
        "⚠️ للعلم: تعليمي فقط"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📚 دليل الاستخدام:\n\n"
        "🎯 الأوامر الأساسية:\n"
        "/start - البدء\n"
        "/help - المساعدة\n"
        "/status - حالة البوت\n\n"
        "💰 إدارة رأس المال:\n"
        "• نسبة مخاطرة: 3%\n"
        "• الحد الأدنى: $100\n"
        "• الحد الأقصى: $500\n\n"
        "📊 المؤشرات:\n"
        "• RSI (14)\n"
        "• MACD (12,26,9)\n"
        "• Bollinger Bands (20,2)\n"
        "• EMA (20,50)\n"
        "• Stochastic (14)\n\n"
        "⏱️ الفريمات:\n"
        "• 1 دقيقة\n"
        "• 5 دقائق\n\n"
        "⚠️ تنبيه مهم:\n"
        "هذه إشارات تعليمية فقط\n"
        "لا تشكل نصيحة مالية\n"
        "تاجر برصيد معقول!"
    )
    await update.message.reply_text(help_text)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send bot status."""
    status_text = (
        "🟢 البوت يعمل بنجاح ✅\n\n"
        "📊 الإحصائيات:\n"
        "├─ الحالة: متصل\n"
        "├─ الرمز: XAUUSD\n"
        "├─ الفريمات: 1m, 5m\n"
        "├─ المؤشرات: 5 مؤشرات\n"
        "├─ المخاطرة: 3%\n"
        "└─ الحساب: $100-$500\n\n"
        "✅ النظام يعمل بشكل طبيعي"
    )
    await update.message.reply_text(status_text)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show balance info."""
    balance_text = (
        "💰 إدارة رأس المال:\n\n"
        "حساب مثال: $250\n"
        "├─ المخاطرة: 3% = $7.50\n"
        "├─ حجم العقد: حسب السعر\n"
        "├─ وقف الخسارة: -1%\n"
        "└─ الهدف: +2%\n\n"
        "⚠️ قاعدة ذهبية:\n"
        "لا تراهن أكثر من 3%"
    )
    await update.message.reply_text(balance_text)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
