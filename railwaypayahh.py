import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) 

def safe_edit(chat_id, msg_id, text):
    try:
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, parse_mode="MarkdownV2")
        return True
    except:
        return False

def mono(text): 
    """Biar semua jadi `kutip telegram`"""
    text = str(text).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    return f"`{text}`"

@bot.message_handler(commands=['start', 'badakin'])
def start_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("▶ START", callback_data="start_badak"))
    bot.send_message(
        message.chat.id,
        mono("=== PANEL BADAK V8 ===\nTekan START untuk eksekusi"),
        reply_markup=markup,
        parse_mode="MarkdownV2"
    )

def get_number_step(message):
    nomor = message.text.strip().replace(" ", "")
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, mono("ERROR: Format nomor harus +62"), parse_mode="MarkdownV2")
        return
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Y", callback_data=f"y|{nomor}"),
        InlineKeyboardButton("X", callback_data="x")
    )
    bot.send_message(
        message.chat.id, 
        mono(f"CONFIRM TARGET:\n{nomor}\n\nApakah sudah benar?"),
        reply_markup=markup,
        parse_mode="MarkdownV2"
    )

@bot.callback_query_handler(func=lambda call: True)
def all_callbacks(call):
    if not call.message: return
    try: bot.answer_callback_query(call.id)
    except: pass 
    msg_id = call.message.id

    if call.data == "start_badak":
        sent = bot.send_message(call.message.chat.id, mono("INPUT TARGET: +62..."), parse_mode="MarkdownV2")
        bot.register_next_step_handler(sent, get_number_step)

    elif call.data == "x":
        safe_edit(call.message.chat.id, msg_id, mono("STATUS: CANCELLED BY USER"))

    elif call.data.startswith("y|"):
        nomor = call.data.split("|", 1)[1]
        run_process(call.message.chat.id, msg_id, nomor)

def run_process(chat_id, msg_id, nomor):
    safe_edit(chat_id, msg_id, mono("[INIT] Starting process..."),)
    steps = [
        "[1/5] CONNECTING TO SERVER...",
        "[2/5] AUTHENTICATING...",
        "[3/5] BYPASSING SECURITY...",
        "[4/5] INJECTING PAYLOAD...",
        "[5/5] FINALIZING..."
    ]
    for i, step in enumerate(steps):
        bar = '█' * (i+1) + '░' * (4-i)
        text = f"{mono(step)}\n{mono(f'[{bar}] {((i+1)*20)}%')}"
        safe_edit(chat_id, msg_id, text)
        time.sleep(1)

    hasil = f"""{mono('=== RESULT ===')}
{mono(f'TARGET : {nomor}')}
{mono('STATUS : SUCCESS')}
{mono('LEVEL : ADMIN ACCESS')}
{mono('EXPIRED : NEVER')}
{mono('================')}
{mono('Run /badakin to repeat')}"""
    safe_edit(chat_id, msg_id, hasil)

if __name__ == '__main__':
    print("Bot V8 Terminal ON")
    bot.infinity_polling(skip_pending=True)
