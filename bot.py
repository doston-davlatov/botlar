import telebot

# Telegram Bot tokenni shu yerga yozing
TOKEN = "8010190605:AAFRCghjyy7frfHKwjUCGmKxfCRTn0YdhRI"
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(TOKEN)
YOUR_TELEGRAM_ID = "1263747123"  # Admin telegram ID

user_states = {}  # Foydalanuvchilar holati
pending_answers = {}  # Yangi savollar uchun mapping

hello_worlds = [
    {"language": "C", "code": '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}'},
    {"language": "C++", "code": '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}'},
    {"language": "Java", "code": 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}'},
    {"language": "Python", "code": 'print("Hello, World!")'},
    {"language": "JavaScript", "code": 'console.log("Hello, World!");'},
    {"language": "C#", "code": 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}'},
    {"language": "PHP", "code": '<?php\necho "Hello, World!";\n?>'},
    {"language": "Ruby", "code": 'puts "Hello, World!"'},
    {"language": "Go", "code": 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}'},
    {"language": "Swift", "code": 'print("Hello, World!")'},
    {"language": "Kotlin", "code": 'fun main() {\n    println("Hello, World!")\n}'},
    {"language": "Rust", "code": 'fn main() {\n    println!("Hello, World!");\n}'},
    {"language": "Perl", "code": 'print "Hello, World!\\n";'},
    {"language": "Scala", "code": 'object HelloWorld {\n    def main(args: Array[String]): Unit = {\n        println("Hello, World!")\n    }\n}'},
    {"language": "Haskell", "code": 'main = putStrLn "Hello, World!"'},
    {"language": "Lua", "code": 'print("Hello, World!")'},
    {"language": "Objective-C", "code": '#import <Foundation/Foundation.h>\n\nint main() {\n    NSLog(@"Hello, World!");\n    return 0;\n}'},
    {"language": "TypeScript", "code": 'console.log("Hello, World!");'},
    {"language": "Shell (Bash)", "code": 'echo "Hello, World!"'},
    {"language": "R", "code": 'cat("Hello, World!\\n")'},
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = None
    bot.reply_to(message, (
        "Xush kelibsiz!\n"
        "Kod namunasi uchun /code\n"
        "Savol berish uchun /question\n"
        "Web-site: /project\n"
        "Admin javobi: /reply <user_id>"
    ))

@bot.message_handler(commands=['code'])
def send_code(message):
    user_states[message.chat.id] = "waiting_for_code"
    languages = "\n".join([f"- {h['language']}" for h in hello_worlds])
    bot.reply_to(message, f"Qaysi dasturlash tilida kod kerak?\nQuyidagilardan birini yozing:\n\n{languages}")

@bot.message_handler(commands=['project'])
def send_project(message):
    bot.reply_to(message, (
        "Web-saytim: https://doston-davlatov.uz\n"
        "Bu yerda turli dasturlash tillari bo'yicha ma'lumot va kodlarni topishingiz mumkin."
    ))

@bot.message_handler(commands=['question'])
def send_question(message):
    user_states[message.chat.id] = "waiting_for_question"
    bot.reply_to(message, "Savolingizni yozing...")

@bot.message_handler(commands=['reply'])
def admin_reply_command(message):
    if str(message.chat.id) != YOUR_TELEGRAM_ID:
        bot.reply_to(message, "❗ Bu buyruq faqat admin uchun.")
        return

    args = message.text.strip().split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        bot.reply_to(message, "❗ Foydalanish: /reply <foydalanuvchi_ID>")
        return

    target_id = int(args[1])
    user_states[message.chat.id] = f"replying_to_{target_id}"
    bot.reply_to(message, f"✏️ Javob matnini yozing. Bu foydalanuvchiga (ID: {target_id}) yuboriladi.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()
    user = message.from_user
    state = user_states.get(chat_id)

    if state == "waiting_for_code":
        matched = next((h for h in hello_worlds if h['language'].lower() == text.lower()), None)
        if matched:
            bot.reply_to(message, f"💻 {matched['language']} Hello World:\n\n```{matched['code']}```", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❗ Bunday dasturlash tili topilmadi. Qaytadan urinib ko'ring.")
        user_states[chat_id] = None

    elif state == "waiting_for_question":
        bot.reply_to(message, f"✅ Savolingiz qabul qilindi: {text}")
        sent = bot.send_message(
            YOUR_TELEGRAM_ID,
            f"🆕 Yangi savol: {text}\n👤 Foydalanuvchi: {user.first_name} (@{user.username}, ID: `{chat_id}`)",
            parse_mode="Markdown"
        )
        pending_answers[sent.message_id] = chat_id
        user_states[chat_id] = None

    elif state and state.startswith("replying_to_") and str(chat_id) == YOUR_TELEGRAM_ID:
        target_id = int(state.split("_")[-1])
        bot.send_message(target_id, f"📩 Admin javobi: {text}")
        bot.reply_to(message, f"✅ Javob foydalanuvchiga yuborildi (ID: {target_id}).")
        user_states[chat_id] = None

    else:
        bot.reply_to(message, "Buyruq tanlang: /start, /code, /project yoki /question.")

if __name__ == "__main__":
    print("Polling boshlanmoqda...")
    bot.infinity_polling()
