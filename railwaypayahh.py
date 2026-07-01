import telebot
import os
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN kosong! Isi di Variables Railway")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=['start', 'badakin'])
def start_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 BADAKIN WA 🔥", callback_data="start_badak"))

    bot.send_message(
        message.chat.id,
        "Selamat datang di Panel BADAKIN WA v99.9\nTekan tombol di bawah untuk memulai.",
        reply_markup=markup
    )

def get_number_step(message):
    nomor = message.text.strip()
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, "Nomor harus pakai awalan `+62` atau `62` jir 😑 Ulangi /badakin")
        return

    # NOMOR LANGSUNG DITEMPEL DI CALLBACK_DATA BIAR GAK PAKE DICT
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Y", callback_data=f"y|{nomor}"),
        InlineKeyboardButton("❌ X", callback_data="x")
    )

    bot.send_message(
        message.chat.id,
        f"Apakah nomor anda sudah benar?\n`{nomor}`",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True) # 1 HANDLER UNTUK SEMUA
def all_callbacks(call):
    bot.answer_callback_query(call.id) # WAJIB PALING ATAS BIAR GAK STUCK

    if call.data == "start_badak":
        sent = bot.send_message(
            call.message.chat.id,
            "Silakan masukkan nomor dengan awalan `+62` atau `62`\n\nContoh: `+628123456789`"
        )
        bot.register_next_step_handler(sent, get_number_step)

    elif call.data == "x":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message_id,
            text="Proses dibatalkan. /badakin lagi kalo mau ngulang 😂"
        )

    elif call.data.startswith("y|"):
        try:
            nomor = call.data.split("|", 1)[1]
        except IndexError:
            bot.edit_message_text("Data error. /badakin lagi 😂", chat_id=call.message.chat.id, message_id=call.message_id)
            return

        run_fake_hack(call.message.chat.id, call.message_id, nomor)

def run_fake_hack(chat_id, msg_id, nomor):
    logs = [
        "Menginisialisasi modul BADAK...",
        "Melewati firewall WhatsApp LLC...",
        "Mendekripsi hash nomor...",
        "Menyuntikkan buff Dewa WA...",
        "Mengoptimalkan sinyal 6G...",
        "Membypass limit Meta..."
    ]

    bot.edit_message_text("`[SYSTEM] Starting...`", chat_id=chat_id, message_id=msg_id)

    for i in range(11):
        percent = i * 10
        bar = '█' * i + '>' + '─' * (10 - i)
        if i == 10: bar = '█' * 10

        log = random.choice(logs) if i < 10 else "Proses Selesai"
        text = f"`[SYSTEM] {log}`\n`[{bar}] {percent}%`"

        try:
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id)
        except telebot.apihelper.ApiTelegramException:
            time.sleep(1) # Kalo kena limit, jeda 1 detik baru lanjut
            continue
        time.sleep(0.6) # 0.6s biar aman dari FloodLimit

    hasil = f"""`[SYSTEM]` ✅ UPGRADE BERHASIL

> Target: `{nomor}`
> Level: Bocil > DEWA WA [Lv.99]
> Buff Aktif:
> - Anti Blokir: ON
> - Centang Biru Palsu: ON
> - Viewer Status: 9999+
> Expired: 3 detik lagi 😂

Tekan /badakin untuk ngulang."""
    bot.edit_message_text(hasil, chat_id=chat_id, message_id=msg_id)

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True, timeout=20)
