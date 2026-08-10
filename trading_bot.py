import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8757189559:AAFw0VLGnEwKBtxqIWwTouB9nJxz6IBPXn0")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 مرحباً! البوت يعمل بنجاح!\n\n"
        "✅ Telegram Bot Trading XAUUSD\n"
        "✅ تحليل فني متقدم\n"
        "✅ إدارة رأس المال\n\n"
        "أرسل: /help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 الأوامر المتاحة:\n\n"
        "/start - البدء\n"
        "/help - المساعدة\n"
        "/status - الحالة\n\n"
        "🤖 البوت يحلل الذهب تلقائياً!"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 البوت يعمل بشكل طبيعي ✅")

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    
    print("🚀 Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
