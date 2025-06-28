import telebot

# BotFather'dan olingan tokenni shu yerga qo'ying
bot = telebot.TeleBot("8010190605:AAFRCghjyy7frfHKwjUCGmKxfCRTn0YdhRI")

# /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Xush kelibsiz! Men veb-dasturlash bo'yicha yordamchingizman. Kod namunasi olish uchun /code, loyiha maslahatlari uchun /project, savollar uchun /question buyrug'ini sinab ko'ring!")

# /code buyrug'i
@bot.message_handler(commands=['code'])
def send_code(message):
    bot.reply_to(message, "Qanday kod namunasi kerak? Masalan, 'CSS flexbox' yoki 'JavaScript funksiyasi' deb yozing.")

# /project buyrug'i
@bot.message_handler(commands=['project'])
def send_project(message):
    bot.reply_to(message, "Loyiha boshqarish bo'yicha maslahat kerakmi? Masalan, 'Agile metodlari' yoki 'vaqtni boshqarish' deb so'rang!")

# /question buyrug'i
@bot.message_handler(commands=['question'])
def send_question(message):
    bot.reply_to(message, "Savolingizni yozing, masalan, 'React nima?' yoki 'API qanday ishlaydi?'")

# Foydalanuvchi oddiy matn yuborsa
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, "Iltimos, buyruqlardan birini ishlating: /start, /code, /project, /question")

# Botni doimiy ishlatish uchun
bot.polling()