import sys
import json
import re
import telebot
from telebot import types
import requests
import threading


DEBUG = "--debug" in sys.argv

positional = [a for a in sys.argv[1:] if not a.startswith("--")]
token_arg        = positional[0] if len(positional) > 0 else None
ai_token_arg = positional[1] if len(positional) > 1 else None


import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_PATH = os.path.join(_ROOT, "data.json")
if os.path.exists(_DATA_PATH):
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}
_DATA2_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data2.json")
if os.path.exists(_DATA2_PATH):
    with open(_DATA2_PATH, "r", encoding="utf-8") as f:
        data2 = json.load(f)
else:
    data2 = {}
TOKEN        = token_arg        or data.get("token")
AI_TOKEN = ai_token_arg or data.get("openrouter_token")

if not TOKEN:
    print(" Токен Telegram не найден")
    sys.exit(1)

if not AI_TOKEN:
    print("OpenRouter-токен не найден")

if DEBUG:
    print(f"[DEBUG] TG токен: {TOKEN[:10]}...")
    print(f"[DEBUG] OpenRouter токен: {'задан' if AI_TOKEN else 'не задан'}")

bot = telebot.TeleBot(TOKEN)


RE_ABOUT    = re.compile(r"о\s*себе",         re.IGNORECASE)
RE_GOAL     = re.compile(r"моя?\s*цель",      re.IGNORECASE)
RE_JOURNEY  = re.compile(r"пришёл\s*в\s*it",  re.IGNORECASE)
RE_MENTOR   = re.compile(r"ментор",           re.IGNORECASE)
RE_PROGRESS = re.compile(r"точка",            re.IGNORECASE)
RE_HOBBIES  = re.compile(r"хобби",            re.IGNORECASE)
RE_WORKS    = re.compile(r"работы",           re.IGNORECASE)
RE_GITHUB   = re.compile(r"github",           re.IGNORECASE)
RE_AI       = re.compile(r"^(спроси|вопрос|ии|ai)\s*[:,]?\s*(.+)", re.IGNORECASE)



def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("1. О себе", "2. Моя цель")
    markup.row("3. Как пришёл в IT", "4. Ментор")
    markup.row("5. Точка А -> Б", "6. Хобби")
    markup.row("7. Мои работы", "8. GitHub")
    markup.row("🤖 Задать вопрос ИИ")
    return markup

def inline_sections():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("👤 О себе",        callback_data="about"),
        types.InlineKeyboardButton("🎯 Цель",           callback_data="goal"),
        types.InlineKeyboardButton("⚡ Путь в IT",      callback_data="journey"),
        types.InlineKeyboardButton("🧑‍🏫 Ментор",        callback_data="mentor"),
        types.InlineKeyboardButton("📈 Прогресс",       callback_data="progress"),
        types.InlineKeyboardButton("🎨 Хобби",          callback_data="hobbies"),
        types.InlineKeyboardButton("🏆 Работы",         callback_data="works"),
        types.InlineKeyboardButton("💻 GitHub",         callback_data="github"),
        types.InlineKeyboardButton("🤖 Спросить ИИ",   callback_data="ai_hint"),
    ]
    markup.add(*buttons)
    return markup


def ask_gemini(question: str) -> str:
    if not AI_TOKEN:
        return "⚠️ OpenRouter не настроен (отсутствует API-ключ)."
    try:
        profile_1 = json.dumps(data, ensure_ascii=False, indent=2)
        profile_2 = json.dumps(data2, ensure_ascii=False, indent=2)

        system_prompt = (
            "Ты — полезный ИИ-ассистент, встроенный в бот-портфолио.\n"
            "Вот официальные данные о владельце портфолио:\n"
            "--- НАЧАЛО ДАННЫХ ---\n"
            f"{profile_1}\n{profile_2}\n"
            "--- КОНЕЦ ДАННЫХ ---\n\n"
            "Правила:\n"
            "1. Отвечай ТОЛЬКО на основе предоставленных данных.\n"
            "2. Не придумывай факты, которых нет в тексте.\n"
            "3. Отвечай коротко и только по-русски.\n"
            "4. Если ответа нет в данных — так и скажи."
        )

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {AI_TOKEN}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "cohere/north-mini-code:free",            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        }

        resp = requests.post(url, headers=headers, json=body, timeout=20)
        resp.raise_for_status()

        result = resp.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⏳ ИИ не ответил вовремя. Попробуй ещё раз."
    except requests.exceptions.HTTPError as http_err:
        return f"❌ Ошибка API: {http_err}"
    except Exception as e:
        if DEBUG:
            print(f"[openrouter] Внутренняя ошибка: {e}")
        return "❌ Не удалось получить ответ от ИИ."


def send_about(chat_id):
    d = data["about"]
    facts = "\n".join(f"• {f}" for f in d["facts"])
    text = (
        f"👤 *{d['name']}*\n"
        f"🗓 {d['age']} лет\n"
        f"💼 {d['role']}\n\n"
        f"*Факты:*\n{facts}"
    )
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_goal(chat_id):
    d = data["goal"]
    text = f"🎯 *Цель:*\n{d['short']}\n\n🚀 *Долгосрочно:*\n{d['long']}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_journey(chat_id):
    steps = "\n\n".join(f"{i+1}. {s}" for i, s in enumerate(data["journey"]))
    text = f"⚡ *Как я пришёл в IT:*\n\n{steps}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_mentor(chat_id):
    d = data["mentor"]
    contribs = "\n".join(f"• {c}" for c in d["contributions"])
    text = f"🧑‍🏫 *Ментор:* {d['name']}\n\n*Чем помог:*\n{contribs}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_progress(chat_id):
    d = data["progress"]
    do  = "\n".join(f"✗ {i}" for i in d["point_a"])
    posle = "\n".join(f"✓ {i}" for i in d["point_b"])
    text = f"📈 *Точка А → Точка Б:*\n\n*Было:*\n{do }\n\n*Стало:*\n{posle}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_hobbies(chat_id):
    items = "\n".join(f"• {h}" for h in data["hobbies"])
    text = f"🎨 *Хобби и интересы:*\n\n{items}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_works(chat_id):
    text = "🏆 *Мои лучшие работы:*\n\n"
    for i, w in enumerate(data["works"]):
        text += f"{i+1}. *{w['title']}*\n{w['description']}\n🔗 {w['link']}\n\n"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())

def send_github(chat_id):
    text = f"💻 *GitHub:*\n\n{data['github']}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(commands=["start"])
def start(message):
    try:
        bot.send_message(
            message.chat.id,
            "👋 Привет! Я портфолио-бот.\n\n"
            "Выбери раздел кнопкой ниже или введи команду:\n"
            "/about · /goal · /journey · /mentor\n"
            "/progress · /hobbies · /works · /github\n\n"
            "Или используй inline-меню 👇",
            reply_markup=main_menu()
        )
        bot.send_message(message.chat.id, " *Разделы:*", parse_mode="Markdown", reply_markup=inline_sections())
    except Exception as e:
        if DEBUG:
            print(f"[start] ошибка: {e}")

@bot.message_handler(commands=["menu"])
def menu(message):
    try:
        bot.send_message(message.chat.id, " *Разделы:*", parse_mode="Markdown", reply_markup=inline_sections())
    except Exception as e:
        if DEBUG:
            print(f"[menu] ошибка: {e}")



@bot.message_handler(commands=["about"])
@bot.message_handler(func=lambda m: bool(RE_ABOUT.search(m.text or "")))
def about(message):
    try: send_about(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[about] {e}")

@bot.message_handler(commands=["goal"])
@bot.message_handler(func=lambda m: bool(RE_GOAL.search(m.text or "")))
def goal(message):
    try: send_goal(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[goal] {e}")

@bot.message_handler(commands=["journey"])
@bot.message_handler(func=lambda m: bool(RE_JOURNEY.search(m.text or "")))
def journey(message):
    try: send_journey(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[journey] {e}")

@bot.message_handler(commands=["mentor"])
@bot.message_handler(func=lambda m: bool(RE_MENTOR.search(m.text or "")))
def mentor(message):
    try: send_mentor(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[mentor] {e}")

@bot.message_handler(commands=["progress"])
@bot.message_handler(func=lambda m: bool(RE_PROGRESS.search(m.text or "")))
def progress(message):
    try: send_progress(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[progress] {e}")

@bot.message_handler(commands=["hobbies"])
@bot.message_handler(func=lambda m: bool(RE_HOBBIES.search(m.text or "")))
def hobbies(message):
    try: send_hobbies(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[hobbies] {e}")

@bot.message_handler(commands=["works"])
@bot.message_handler(func=lambda m: bool(RE_WORKS.search(m.text or "")))
def works(message):
    try: send_works(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[works] {e}")

@bot.message_handler(commands=["github"])
@bot.message_handler(func=lambda m: bool(RE_GITHUB.search(m.text or "")))
def github(message):
    try: send_github(message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[github] {e}")



@bot.message_handler(func=lambda m: m.text == "🤖 Задать вопрос ИИ")
def ai_prompt(message):
    try:
        bot.send_message(
            message.chat.id,
            " Напиши свой вопрос обо мне, и Gemini ответит!\n\n"
            "Например: *Какие языки программирования ты знаешь?*\n"
            "Или напиши: `вопрос: <твой вопрос>`",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    except Exception as e:
        if DEBUG: print(f"[ai_prompt] {e}")

@bot.message_handler(commands=["ask"])
def ask_command(message):
    try:
        question = message.text.replace("/ask", "").strip()
        if not question:
            bot.send_message(message.chat.id, "Напиши вопрос после команды: `/ask Чем ты занимаешься?`", parse_mode="Markdown")
            return
        msg = bot.send_message(message.chat.id, "⏳ Думаю...")
        def run(q, chat_id, msg_id):
            answer = ask_gemini(q)
            try:
                bot.edit_message_text(f"🤖 *ИИ отвечает:*\n\n{answer}", chat_id, msg_id, parse_mode="Markdown")
            except Exception as ex:
                if DEBUG: print(f"[ask edit] {ex}")
        threading.Thread(target=run, args=(question, message.chat.id, msg.message_id), daemon=True).start()
    except Exception as e:
        if DEBUG: print(f"[ask] {e}")

@bot.message_handler(func=lambda m: bool(RE_AI.match(m.text or "")))
def ai_text(message):
    try:
        match = RE_AI.match(message.text)
        question = match.group(2).strip()
        msg = bot.send_message(message.chat.id, "⏳ Думаю...")
        def run(q, chat_id, msg_id):
            answer = ask_gemini(q)
            try:
                bot.edit_message_text(f"🤖 *ИИ отвечает:*\n\n{answer}", chat_id, msg_id, parse_mode="Markdown")
            except Exception as ex:
                if DEBUG: print(f"[ai_text edit] {ex}")
        threading.Thread(target=run, args=(question, message.chat.id, msg.message_id), daemon=True).start()
    except Exception as e:
        if DEBUG: print(f"[ai_text] {e}")



CALLBACKS = {
    "about":    send_about,
    "goal":     send_goal,
    "journey":  send_journey,
    "mentor":   send_mentor,
    "progress": send_progress,
    "hobbies":  send_hobbies,
    "works":    send_works,
    "github":   send_github,
}

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        bot.answer_callback_query(call.id)
        if call.data == "ai_hint":
            bot.send_message(
                call.message.chat.id,
                " Напиши вопрос в формате:\n`вопрос: <твой вопрос>`\nили команду `/ask <вопрос>`",
                parse_mode="Markdown",
                reply_markup=main_menu()
            )
        elif call.data in CALLBACKS:
            CALLBACKS[call.data](call.message.chat.id)
    except Exception as e:
        if DEBUG: print(f"[callback] {e}")



@bot.message_handler(func=lambda m: True)
def unknown(message):
    try:
        bot.send_message(
            message.chat.id,
            "Не понял  Выбери раздел из меню или введи /start\n\n"
            "Чтобы задать вопрос ИИ: `вопрос: <твой вопрос>`",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    except Exception as e:
        if DEBUG: print(f"[unknown] {e}")



if __name__ == "__main__":
    if DEBUG:
        print("[DEBUG] Режим отладки включён")
    bot.polling(none_stop=True)