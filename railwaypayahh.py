import telebot
import os
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN kosong! Isi di Variables Railway")

# MarkdownV2 dimatiin biar gak ribut sama \. \n
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) 

def safe_edit(chat_id, msg_id, text):
    """Fungsi anti crash pas edit message"""
    try:
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id)
        return True
    except ApiTelegramException as e:
        if "message is not modified" in str(e).lower():
            return True 
        if "Flood wait" in str(e):
            time.sleep(2)
            return safe_edit(chat_id, msg_id, text)
        print(f"EDIT ERROR: {e}")
        return False

@bot.message_handler(commands=['start', 'badakin'])
def start_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 BADAKIN WA 🔥", callback_data="start_badak"))
    bot.send_message(
        message.chat.id,
        "Selamat datang di Panel TEST V5\nTekan tombol di bawah untuk memulai.", # Ganti nama biar aman
        reply_markup=markup
    )

def get_number_step(message):
    nomor = message.text.strip().replace(" ", "")
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, "Nomor harus pakai awalan +62 atau 62. Ulangi /badakin")
        return

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Y", callback_data=f"y|{nomor}"),
        InlineKeyboardButton("❌ X", callback_data="x")
    )
    bot.send_message(
        message.chat.id,
        f"Apakah nomor anda sudah benar?\n{nomor}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def all_callbacks(call):
    if not call.message: return # ANTI CRASH KALO GAK ADA MESSAGE
    try:
        bot.answer_callback_query(call.id) # Biar tombol gak muter
    except:
        pass 

    if call.data == "start_badak":
        sent = bot.send_message(
            call.message.chat.id,
            "Silakan masukkan nomor dengan awalan +62 atau 62\nContoh: +628123456789"
        )
        bot.register_next_step_handler(sent, get_number_step)

    elif call.data == "x":
        # INI YANG TADI ERROR. UDAH FIX PAKE.message_id
        safe_edit(call.message.chat.id, call.message_id, "Proses dibatalkan. /badakin lagi kalo mau ngulang 😂")

    elif call.data.startswith("y|"):
        try:
            nomor = call.data.split("|", 1)[1]
            # INI JUGA UDAH FIX PAKE.message_id
            run_fake_hack(call.message.chat.id, call.message_id, nomor) 
        except Exception as e:
            safe_edit(call.message.chat.id, call.message_id, f"Data error: {e}. /badakin lagi 😂")

def run_fake_hack(chat_id, msg_id, nomor):
    logs = [
        "Menginisialisasi modul...",
        "Melewati firewall WhatsApp...",
        "Mendekripsi hash nomor...",
        "Menyuntikkan buff Dewa WA...",
        "Mengoptimalkan sinyal 6G...",
        "Membypass limit Meta..."
    ]

    safe_edit(chat_id, msg_id, "[SYSTEM] Starting...")

    for i in range(11):
        percent = i * 10
        bar = '█' * i + '>' + '─' * (10 - i)
        if i == 10: bar = '█' * 10
        log = random.choice(logs) if i < 10 else "Proses Selesai"
        text = f"[SYSTEM] {log}\n[{bar}] {percent}%"
        safe_edit(chat_id, msg_id, text)
        time.sleep(0.7)

    hasil = f"""[SYSTEM] ✅ UPGRADE BERHASIL

> Target: {nomor}
> Level: Bocil > DEWA WA [Lv.99]
> Buff Aktif:
> - Anti Blokir: ON
> - Centang Biru Palsu: ON
> - Viewer Status: 9999+
> Expired: 3 detik lagi 😂

Tekan /badakin untuk ngulang."""
    safe_edit(chat_id, msg_id, hasil)

if __name__ == '__main__':
    print("Bot V6.2 Anti Crash ON")
    bot.infinity_polling(skip_pending=True, none_stop=True, timeout=60, long_polling_timeout=60)
