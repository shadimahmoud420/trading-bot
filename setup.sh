#!/bin/bash

# 🚀 سكريبت تثبيت وتشغيل بوت تحليل الذهب
# Gold Trading Analysis Bot Setup Script

echo "╔════════════════════════════════════╗"
echo "║   🤖 بوت تحليل الذهب - التثبيت    ║"
echo "║   Gold Trading Bot - Setup         ║"
echo "╚════════════════════════════════════╝"
echo ""

# 1. التحقق من Python
echo "📋 التحقق من Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    echo "الرجاء تثبيت Python 3.8 أو أعلى"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo ""

# 2. إنشاء بيئة افتراضية (اختياري)
echo "🔧 إنشاء بيئة افتراضية..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ تم إنشاء البيئة الافتراضية"
else
    echo "ℹ️ البيئة الافتراضية موجودة بالفعل"
fi
echo ""

# 3. تفعيل البيئة الافتراضية
echo "⚙️ تفعيل البيئة الافتراضية..."
source venv/bin/activate
echo "✅ تم التفعيل"
echo ""

# 4. تحديث pip
echo "📦 تحديث pip..."
pip install --upgrade pip --quiet
echo "✅ تم التحديث"
echo ""

# 5. تثبيت المكتبات المطلوبة
echo "📚 تثبيت المكتبات المطلوبة..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ تم تثبيت جميع المكتبات"
else
    echo "❌ ملف requirements.txt غير موجود"
    exit 1
fi
echo ""

# 6. التحقق من الملفات المطلوبة
echo "📁 التحقق من الملفات المطلوبة..."
required_files=("trading_bot.py" "config.py" "indicators.py" "README.md")
all_exist=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file موجود"
    else
        echo "❌ $file غير موجود"
        all_exist=false
    fi
done

if [ "$all_exist" = false ]; then
    echo ""
    echo "❌ بعض الملفات المطلوبة غير موجودة"
    echo "تأكد من وجود جميع الملفات في المجلد الحالي"
    exit 1
fi
echo ""

# 7. إنشاء ملف .env
echo "🔐 إعداد متغيرات البيئة..."
if [ ! -f ".env" ]; then
    echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > .env
    echo "✅ تم إنشاء ملف .env"
    echo "⚠️  قم بتعديل .env وأضف Bot Token الخاص بك"
else
    echo "ℹ️ ملف .env موجود بالفعل"
fi
echo ""

# 8. عرض التعليمات التالية
echo "╔════════════════════════════════════╗"
echo "║   ✅ اكتمل التثبيت بنجاح!         ║"
echo "╚════════════════════════════════════╝"
echo ""
echo "📝 الخطوات التالية:"
echo ""
echo "1️⃣  عدّل ملف config.py وأضف Bot Token:"
echo "   TELEGRAM_BOT_TOKEN = 'your_token_here'"
echo ""
echo "2️⃣  شغّل البوت:"
echo "   python trading_bot.py"
echo ""
echo "3️⃣  أضف البوت إلى محادثتك في التليجرام:"
echo "   @TradingbyshadiBot"
echo ""
echo "4️⃣  ابدأ مع البوت:"
echo "   /start"
echo ""
echo "📚 للمزيد من المعلومات: اقرأ README.md"
echo ""
echo "⚠️  تذكر: هذه الإشارات لأغراض تعليمية فقط!"
echo ""
