import telebot
import os
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) 

def safe_edit(chat_id, msg_id, text):
    try:
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id)
        return True
    except:
        return False

@bot.message_handler(commands=['start', 'badakin'])
def start_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 BADAKIN WA 🔥", callback_data="start_badak"))
    bot.send_message(message.chat.id, "Panel TEST V7\nTekan tombol di bawah.", reply_markup=markup)

def get_number_step(message):
    nomor = message.text.strip().replace(" ", "")
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, "Nomor harus +62. /badakin lagi")
        return
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Y", callback_data=f"y|{nomor}"),
        InlineKeyboardButton("❌ X", callback_data="x")
    )
    bot.send_message(message.chat.id, f"Nomor bener? \n{nomor}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def all_callbacks(call):
    if not call.message: return
    try: bot.answer_callback_query(call.id)
    except: pass 

    msg_id = call.message.id # <-- INI KUNCINYA. AMBIL DARI SINI

    if call.data == "start_badak":
        sent = bot.send_message(call.message.chat.id, "Masukin nomor +62")
        bot.register_next_step_handler(sent, get_number_step)

    elif call.data == "x":
        safe_edit(call.message.chat.id, msg_id, "Dibatalkan 😂") # PAKE msg_id

    elif call.data.startswith("y|"):
        nomor = call.data.split("|", 1)[1]
        run_fake_hack(call.message.chat.id, msg_id, nomor) # PAKE msg_id

def run_fake_hack(chat_id, msg_id, nomor):
    safe_edit(chat_id, msg_id, "[SYSTEM] Starting...")
    for i in range(11):
        percent = i * 10
        bar = '█' * i + '>' + '─' * (10 - i)
        if i == 10: bar = '█' * 10
        text = f"[SYSTEM] Loading...\n[{bar}] {percent}%"
        safe_edit(chat_id, msg_id, text)
        time.sleep(0.5)
    hasil = f"[SYSTEM] ✅ SELESAI\n> Target: {nomor}\nTekan /badakin"
    safe_edit(chat_id, msg_id, hasil)

if __name__ == '__main__':
    print("Bot V7 ON")
    bot.infinity_polling(skip_pending=True)
