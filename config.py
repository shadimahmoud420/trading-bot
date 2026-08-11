# ⚙️ إعدادات Telegram Trading Bot
# Configuration for Gold (XAUUSD) Trading Analysis Bot

# 🔑 بيانات التليجرام
TELEGRAM_BOT_TOKEN = "8757189559:AAFw0VLGnEwKBtxqIWwTouB9nJxz6IBPXn0"

# 💰 إعدادات إدارة رأس المال
ACCOUNT_BALANCE_MIN = 100  # الحد الأدنى للحساب ($)
ACCOUNT_BALANCE_MAX = 500  # الحد الأقصى للحساب ($)
RISK_PERCENTAGE = 0.03  # نسبة المخاطرة (3%)

# 📊 إعدادات التحليل الفني
SYMBOL = "XAUUSD"  # رمز الذهب
TIMEFRAMES = ["1m", "5m"]  # الفريمات الزمنية

# 🎯 إعدادات المؤشرات الفنية
INDICATORS_CONFIG = {
    "RSI": {
        "period": 14,
        "overbought": 70,
        "oversold": 30
    },
    "MACD": {
        "fast": 12,
        "slow": 26,
        "signal": 9
    },
    "BOLLINGER": {
        "period": 20,
        "std_dev": 2
    },
    "EMA": {
        "fast": 20,
        "slow": 50
    },
    "STOCHASTIC": {
        "period": 14,
        "smooth_k": 3,
        "smooth_d": 3
    }
}

# 🔔 إعدادات الإشارات
SIGNAL_THRESHOLD = 0.65  # نسبة اتفاق المؤشرات للإشارة
UPDATE_INTERVAL = 60  # تحديث كل 60 ثانية

# 📈 إعدادات الإشعارات
SEND_ALL_UPDATES = True  # إرسال لجميع المستخدمين عند الإشارات
STORE_SIGNALS = True  # حفظ الإشارات في قاعدة بيانات

# 🛡️ الإعدادات الأمنية
LOG_SIGNALS = True  # تسجيل الإشارات
DEBUG_MODE = False  # وضع التصحيح
