#!/bin/bash
# سكربت تشغيل بوت الحماية تلقائي
# ابن اليمن - إعداد خاص

# 1) تحديد مجلد البوت (عدّل لو مش في نفس المسار)
BOT_DIR="$(pwd)"

# 2) إنشاء بيئة افتراضية إذا مش موجودة
if [ ! -d "$BOT_DIR/.venv" ]; then
  echo "⚙️ إنشاء بيئة افتراضية..."
  python3 -m venv "$BOT_DIR/.venv"
fi

# 3) تفعيل البيئة
source "$BOT_DIR/.venv/bin/activate"

# 4) ترقية pip
echo "⚙️ ترقية pip..."
pip install --upgrade pip

# 5) تثبيت المكتبات
echo "⚙️ تثبيت المكتبات المطلوبة..."
cat > "$BOT_DIR/requirements.txt" <<EOF
pyrogram
tgcrypto
yt-dlp
youtube-search
SpeechRecognition
requests
asSQL
dragonxxdlib
getids
EOF

pip install -r "$BOT_DIR/requirements.txt"

# 6) تشغيل البوت
echo "🚀 تشغيل البوت الآن..."
python3 "$BOT_DIR/main.py"