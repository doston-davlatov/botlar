import telebot
import os

# Bot tokenini environment o'zgaruvchisidan olish
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN muhit o'zgaruvchisi topilmadi! Render yoki .env faylda uni o'rnating.")

bot = telebot.TeleBot(TOKEN)

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
    bot.reply_to(message, (
        "Xush kelibsiz! Men veb-dasturlash bo'yicha yordamchingizman.\n"
        "Kod namunasi olish uchun /code, loyiha maslahatlari uchun /project, "
        "savollar uchun /question buyrug'ini sinab ko'ring!"
    ))

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

# /reply buyrug'i (admin uchun foydalanuvchiga javob yuborish)
@bot.message_handler(commands=['reply'])
def send_reply(message):
    if str(message.chat.id) == YOUR_TELEGRAM_ID:
        parts = message.text.split(maxsplit=2)
        if len(parts) >= 3:
            user_id = int(parts[1])
            reply_text = parts[2]
            if user_id in user_queries:
                bot.send_message(user_id, f"Javob: {reply_text}")
                bot.reply_to(message, f"Javob muvaffaqiyatli {user_id} ga yuborildi!")
            else:
                bot.reply_to(message, "Bu foydalanuvchi topilmadi yoki savol yo'q.")
        else:
            bot.reply_to(message, "Iltimos, /reply <user_id> <javob> formatida yozing.\nMasalan: /reply 123456789 Salom!")
    else:
        bot.reply_to(message, "Sizda bu buyruqni ishlatish huquqi yo'q.")

# Oddiy matnlarni qabul qilish
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    user = message.from_user

    state = user_states.get(chat_id)
    if state == "waiting_for_code":
        if "css" in text.lower():
            bot.reply_to(message, "CSS flexbox namunasi:\n```\n.display-flex {\n  display: flex;\n  justify-content: center;\n}\n```")
        elif "javascript" in text.lower():
            bot.reply_to(message, "JavaScript funksiyasi namunasi:\n```\nfunction greet() {\n  return 'Salom!';\n}\n```")
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
        user_info = f"{user.first_name} (@{user.username if user.username else 'no_username'}, ID: {chat_id})"
        bot.reply_to(message, "Sizning savolingiz qabul qilindi: " + text)
        bot.send_message(YOUR_TELEGRAM_ID, f"Yangi savol: {text}\nFoydalanuvchi: {user_info}")
        user_queries[chat_id] = text
        user_states[chat_id] = None

    else:
        bot.reply_to(message, "Iltimos, buyruqlardan birini ishlating: /start, /code, /project, /question")

# Botni ishga tushirish
bot.polling()
