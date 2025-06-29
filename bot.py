import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi, uni .env faylga yozing yoki Render muhit o‘zgaruvchisi sifatida qo‘shing!")

bot = telebot.TeleBot(TOKEN)

YOUR_TELEGRAM_ID = "1263747123"
user_states = {}
user_queries = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = None
    bot.reply_to(message, (
        "Xush kelibsiz! Men polling rejimida ishlayapman.\n"
        "Kod namunasi uchun /code, loyiha maslahatlari uchun /project, savollar uchun /question."
    ))

@bot.message_handler(commands=['code'])
def send_code(message):
    user_states[message.chat.id] = "waiting_for_code"
    bot.reply_to(message, "Qanday kod namunasi kerak? Masalan, 'CSS flexbox' yoki 'JavaScript funksiyasi'...")

@bot.message_handler(commands=['question'])
def send_question(message):
    user_states[message.chat.id] = "waiting_for_question"
    bot.reply_to(message, "Savolingizni yozing...")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    user = message.from_user
    state = user_states.get(chat_id)
    if state == "waiting_for_code":
        bot.reply_to(message, "Kod namunasi shu yerda (demo).")
        user_states[chat_id] = None
    elif state == "waiting_for_question":
        bot.reply_to(message, f"Sizning savolingiz qabul qilindi: {text}")
        bot.send_message(YOUR_TELEGRAM_ID, f"Yangi savol: {text}\nFoydalanuvchi: {user.first_name} (@{user.username}, ID: {chat_id})")
        user_states[chat_id] = None
    else:
        bot.reply_to(message, "Buyruq tanlang: /start, /code yoki /question.")

if __name__ == "__main__":
    print("Polling boshlanmoqda...")
    bot.infinity_polling()
