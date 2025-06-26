from telegram import Bot
from datetime import datetime
import schedule
import time
from flask import Flask
import threading

# بيانات البوت
TOKEN = "8127971390:AAH-OQPec02p6niyz83z9LnWFsqBA-OL98w"
CHANNEL_ID = "@spindarfs"

bot = Bot(token=TOKEN)

# الوظيفة اللي تبعت الاستفتاء
def send_poll():
    today = datetime.now().strftime("%d-%m-%Y")
    question = f"📅 هل أنجزت المهام اليوم؟ ({today})"
    options = [
        "✅ استلام الوردية",
        "✅ كتابة التقرير"
    ]
    try:
        bot.send_poll(
            chat_id=CHANNEL_ID,
            question=question,
            options=options,
            is_anonymous=True,
            allows_multiple_answers=True
        )
        print("✅ تم إرسال الاستفتاء")
    except Exception as e:
        print("🚨 خطأ أثناء الإرسال:", e)

# جدول التنفيذ
schedule.every(5).minutes.do(send_poll)
send_poll()  # أول إرسال تجريبي

# تشغيل الجدولة في خيط مستقل
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# إعداد Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "بوت المهام شغال ✅"

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)