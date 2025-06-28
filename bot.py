import telebot
import os

# Bot tokenini environment o'zgaruvchisidan olish
bot = telebot.TeleBot(os.getenv("8010190605:AAFRCghjyy7frfHKwjUCGmKxfCRTn0YdhRI"))

# Sizning Telegram ID'ingiz
YOUR_TELEGRAM_ID = "1263747123"

# Foydalanuvchi holatini saqlash uchun global o'zgaruvchi
user_states = {}

# Foydalanuvchi savollari va javoblarni saqlash uchun global lug'at
user_queries = {}

# /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = None
    bot.reply_to(message, "Xush kelibsiz! Men veb-dasturlash bo'yicha yordamchingizman. Kod namunasi olish uchun /code, loyiha maslahatlari uchun /project, savollar uchun /question buyrug'ini sinab ko'ring!")

# /code buyrug'i
@bot.message_handler(commands=['code'])
def send_code(message):
    user_states[message.chat.id] = "waiting_for_code"
    bot.reply_to(message, "Qanday kod namunasi kerak? Masalan, 'CSS flexbox' yoki 'JavaScript funksiyasi' ...")

# /project buyrug'i
@bot.message_handler(commands=['project'])
def send_project(message):
    user_states[message.chat.id] = "waiting_for_project"
    bot.reply_to(message, "Loyiha boshqarish bo'yicha maslahat kerakmi? Masalan, 'Agile metodlari' yoki 'vaqtni boshqarish' ...")

# /question buyrug'i
@bot.message_handler(commands=['question'])
def send_question(message):
    user_states[message.chat.id] = "waiting_for_question"
    bot.reply_to(message, "Savolingizni yozing ...")

# /reply buyrug'i (siz uchun foydalanuvchiga javob yozish)
@bot.message_handler(commands=['reply'])
def send_reply(message):
    if message.chat.id == int(YOUR_TELEGRAM_ID):
        try:
            parts = message.text.split(maxsplit=1)
            if len(parts) > 1:
                user_id = int(parts[0].replace('/reply ', ''))
                reply_text = parts[1]
                if user_id in user_queries:
                    bot.send_message(user_id, f"Javob: {reply_text}")
                    bot.reply_to(message, f"Javob muvaffaqiyatli {user_id} ga yuborildi!")
                else:
                    bot.reply_to(message, "Bu foydalanuvchi topilmadi yoki savol yo'q.")
            else:
                bot.reply_to(message, "Iltimos, /reply <user_id> <javob> formatida yozing, masalan: /reply 123456789 Salom!")
        except ValueError:
            bot.reply_to(message, "Foydalanuvchi ID'si noto'g'ri. Raqam kiriting!")

# Oddiy matnni qabul qilish
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    user = message.from_user

    if chat_id in user_states:
        state = user_states[chat_id]

        if state == "waiting_for_code":
            if "css" in text.lower():
                bot.reply_to(message, "CSS flexbox namunasi:\n```css\n.display-flex {\n  display: flex;\n  justify-content: center;\n}\n```")
            elif "javascript" in text.lower():
                bot.reply_to(message, "JavaScript funksiyasi namunasi:\n```javascript\nfunction greet() {\n  return 'Salom!';\n}\n```")
            else:
                bot.reply_to(message, "Aniqroq so'rov kiriting, masalan, 'CSS flexbox' yoki 'JavaScript funksiyasi'.")
            user_states[chat_id] = None

        elif state == "waiting_for_project":
            if "agile" in text.lower():
                bot.reply_to(message, "Agile - loyiha boshqarish metodologiyasi, iteratsiyali rivojlanishni o'z ichiga oladi.")
            elif "vaqt" in text.lower():
                bot.reply_to(message, "Vaqtni boshqarish uchun Pomodoro texnikasini sinab ko'ring.")
            else:
                bot.reply_to(message, "Aniqroq so'rov kiriting, masalan, 'Agile metodlari'.")
            user_states[chat_id] = None

        elif state == "waiting_for_question":
            user_info = f"{user.first_name} (@{user.username} if available, ID: {chat_id})"
            if user.username:
                user_info = f"{user.first_name} (@{user.username}, ID: {chat_id})"
            bot.reply_to(message, "Sizning savolingiz qabul qilindi: " + text)
            bot.send_message(YOUR_TELEGRAM_ID, f"Yangi savol: {text} (Foydalanuvchi: {user_info})")
            user_queries[chat_id] = text  # Savolni saqlash
            user_states[chat_id] = None

        else:
            bot.reply_to(message, "Iltimos, buyruqlardan birini ishlating: /start, /code, /project, /question")
    else:
        bot.reply_to(message, "Iltimos, /start bilan boshlang!")

# Botni doimiy ishlatish uchun
bot.polling()