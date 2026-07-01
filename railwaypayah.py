import telebot
import os
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# GAK PAKE DICT GLOBAL LAGI BIAR AMAN DI RAILWAY
# DATA NOMOR NYA GWE TEMPEL DI MESSAGE AJA

@bot.message_handler(commands=['start', 'badakin'])
def start_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 BADAKIN WA 🔥", callback_data="start_badak"))

    bot.send_message(
        message.chat.id,
        "Selamat datang di Panel BADAKIN WA v99.9\nTekan tombol di bawah untuk memulai.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "start_badak")
def ask_number(call):
    bot.answer_callback_query(call.id)
    sent = bot.send_message(
        call.message.chat.id,
        "Silakan anda memasukkan nomor dengan awalan `+62` atau `62`\n\nContoh: `+628123456789`",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(sent, get_number_step)

def get_number_step(message):
    nomor = message.text.strip()
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, "Nomor harus pakai awalan `+62` atau `62` jir 😑 Ulangi /badakin")
        return

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Y", callback_data=f"confirm_y|{nomor}"), # NOMOR GWE TEMPEL DI SINI
        InlineKeyboardButton("❌ X", callback_data="confirm_x")
    )

    bot.send_message(
        message.chat.id,
        f"Apakah nomor anda sudah benar?\n`{nomor}`",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm"))
def confirm_step(call):
    bot.answer_callback_query(call.id)

    if call.data == "confirm_x":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message_id,
            text="Proses dibatalkan. /badakin lagi kalo mau ngulang 😂"
        )
        return

    # AMBIL NOMOR DARI CALLBACK_DATA, JADI GAK DEPENDE KE DICT
    try:
        nomor = call.data.split("|")[1]
    except IndexError:
        bot.edit_message_text("Data error jir. /badakin lagi 😂", chat_id=call.message.chat.id, message_id=call.message_id)
        return

    run_fake_hack(call, nomor)

def run_fake_hack(call, nomor):
    logs = [
        "Menginisialisasi modul BADAK...",
        "Melewati firewall WhatsApp LLC...",
        "Mendekripsi hash nomor...",
        "Menyuntikkan buff Dewa WA...",
        "Mengoptimalkan sinyal 6G...",
        "Membypass limit Meta..."
    ]

    msg = bot.edit_message_text("`[SYSTEM] Starting...`", chat_id=call.message.chat.id, message_id=call.message_id, parse_mode='Markdown')

    for i in range(11):
        percent = i * 10
        bar = '█' * i + '>' + '─' * (10 - i)
        if i == 10: bar = '█' * 10

        log = random.choice(logs) if i < 10 else "Proses Selesai"
        text = f"`[SYSTEM] {log}`\n`[{bar}] {percent}%`"

        try:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=msg.message_id, parse_mode='Markdown')
        except telebot.apihelper.ApiTelegramException:
            pass # Skip kalo editnya kecepetan / kena limit
        time.sleep(0.5)

    hasil = f"""
`[SYSTEM]` ✅ UPGRADE BERHASIL

> Target: `{nomor}`
> Level: Bocil > DEWA WA [Lv.99]
> Buff Aktif:
> - Anti Blokir: ON
> - Centang Biru Palsu: ON
> - Viewer Status: 9999+
> Expired: 3 detik lagi 😂

Tekan /badakin untuk ngulang.
    """
    bot.edit_message_text(hasil, chat_id=call.message.chat.id, message_id=msg.message_id, parse_mode='Markdown')

if __name__ == '__main__':
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
