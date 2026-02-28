import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

TOKEN = "8029572892:AAHjpiaclLWSRqx7sl3oXC5ZtUBflb9iV-o"
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(TOKEN)
YOUR_TELEGRAM_ID = "1263747123"  

user_states = {}  
pending_answers = {}  

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

languages_per_page = 8
total_pages = (len(hello_worlds) + languages_per_page - 1) // languages_per_page

def create_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💻 Kod namunasi", callback_data="menu_code"),
        InlineKeyboardButton("❓ Savol yuborish", callback_data="menu_question")
    )
    markup.add(
        InlineKeyboardButton("🌐 Mening saytim", callback_data="menu_project"),
        InlineKeyboardButton("🆘 Yordam / About", callback_data="menu_help")
    )
    return markup

def create_language_pagination(page=1):
    markup = InlineKeyboardMarkup(row_width=2)
    start = (page - 1) * languages_per_page
    end = min(start + languages_per_page, len(hello_worlds))
    
    for i in range(start, end, 2):
        row = []
        row.append(InlineKeyboardButton(
            hello_worlds[i]['language'],
            callback_data=f"lang_{hello_worlds[i]['language']}"
        ))
        if i + 1 < end:
            row.append(InlineKeyboardButton(
                hello_worlds[i+1]['language'],
                callback_data=f"lang_{hello_worlds[i+1]['language']}"
            ))
        markup.add(*row)
    
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("◀️ Oldingi", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton(f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("Keyingi ▶️", callback_data=f"page_{page+1}"))
    markup.add(*nav)
    
    markup.add(InlineKeyboardButton("🏠 Bosh menyuga", callback_data="back_main"))
    
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = None
    text = (
        "Assalomu alaykum! 👋\n"
        "Men dasturlash tillari bo‘yicha Hello World misollarini beraman,\n"
        "savollaringizga javob berishga yordam beraman."
    )
    bot.reply_to(message, text, reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data

    if data == "noop":
        bot.answer_callback_query(call.id)
        return

    if data == "back_main":
        bot.edit_message_text(
            "Bosh menyuga qaytdingiz ✓",
            chat_id, msg_id,
            reply_markup=create_main_menu()
        )
        bot.answer_callback_query(call.id, "Bosh sahifa")
        return

    if data.startswith("menu_"):
        action = data.split("_")[1]
        
        if action == "code":
            bot.edit_message_text(
                "Qaysi tilda kod kerak? Tanlang:",
                chat_id, msg_id,
                reply_markup=create_language_pagination(1)
            )
        elif action == "question":
            user_states[chat_id] = "waiting_for_question"
            bot.edit_message_text(
                "Savolingizni yozing... ✍️\n\n(javob tez orada keladi)",
                chat_id, msg_id,
                reply_markup=create_main_menu()
            )
        elif action == "project":
            bot.edit_message_text(
                "Web-saytim: https://doston-davlatov.uz\n\nKodlar va maqolalar bor!",
                chat_id, msg_id,
                reply_markup=create_main_menu()
            )
        elif action == "help":
            help_text = (
                "Mavjud imkoniyatlar:\n\n"
                "• Kod namunasi — turli tillarda Hello World\n"
                "• Savol yuborish — admin javob beradi\n"
                "• Sayt — qo‘shimcha materiallar"
            )
            bot.edit_message_text(help_text, chat_id, msg_id, reply_markup=create_main_menu())
        
        bot.answer_callback_query(call.id)
        return

    if data.startswith("page_"):
        page = int(data.split("_")[1])
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=create_language_pagination(page)
        )
        bot.answer_callback_query(call.id, f"Sahifa {page}")
        return

    if data.startswith("lang_"):
        lang_name = data.split("_", 1)[1]
        matched = next((h for h in hello_worlds if h['language'] == lang_name), None)
        if matched:
            code_text = f"💻 {matched['language']} — Hello, World!\n\n```{matched['code']}```"
            bot.edit_message_text(
                code_text,
                chat_id, msg_id,
                parse_mode="Markdown",
                reply_markup=create_main_menu()
            )
            bot.answer_callback_query(call.id, f"{lang_name} tanlandi!")
        else:
            bot.answer_callback_query(call.id, "Xato: til topilmadi", show_alert=True)
        user_states[chat_id] = None
        return

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()
    user = message.from_user
    state = user_states.get(chat_id)

    if state == "waiting_for_question":
        bot.reply_to(message, f"✅ Savolingiz qabul qilindi: {text}\nJavobni kuting...")
        sent = bot.send_message(
            YOUR_TELEGRAM_ID,
            f"🆕 Yangi savol: {text}\n👤 Foydalanuvchi: {user.first_name} (@{user.username if user.username else 'yo‘q'}, ID: `{chat_id}`)",
            parse_mode="Markdown"
        )
        pending_answers[sent.message_id] = chat_id
        user_states[chat_id] = None
        bot.send_message(chat_id, "Bosh menyuga qaytish uchun /start bosing", reply_markup=create_main_menu())
        return

    if state and state.startswith("replying_to_") and str(chat_id) == YOUR_TELEGRAM_ID:
        target_id = int(state.split("_")[-1])
        bot.send_message(target_id, f"📩 Admin javobi:\n\n{text}")
        bot.reply_to(message, f"✅ Javob yuborildi (ID: {target_id})")
        user_states[chat_id] = None
        return

    bot.reply_to(message, "Iltimos, menyudan foydalaning 👆", reply_markup=create_main_menu())

@bot.message_handler(commands=['reply'])
def admin_reply_command(message):
    if str(message.chat.id) != YOUR_TELEGRAM_ID:
        return
    args = message.text.strip().split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        bot.reply_to(message, "Foydalanish: /reply <user_id>")
        return
    target_id = int(args[1])
    user_states[message.chat.id] = f"replying_to_{target_id}"
    bot.reply_to(message, f"Javob matnini yozing (foydalanuvchi ID: {target_id})")

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()