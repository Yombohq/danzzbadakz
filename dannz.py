import os
import telebot
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# PENTING: Ambil token dari Railway Variables, bukan hardcode
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Simpan data sementara user. key = user_id
user_data = {}

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
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message_id,
        text="Silakan anda memasukkan nomor dengan awalan `+62` atau `62`\n\nContoh: `+628123456789`",
        parse_mode='Markdown',
        reply_markup=None # Hapus tombol
    )
    bot.register_next_step_handler(call.message, get_number_step)

def get_number_step(message):
    nomor = message.text.strip()
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, "Nomor harus pakai awalan `+62` atau `62` jir 😑 Ulangi /badakin")
        return

    user_data[message.from_user.id] = {'nomor': nomor}

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Y", callback_data="confirm_y"),
        InlineKeyboardButton("❌ X", callback_data="confirm_x")
    )
    
    bot.send_message(
        message.chat.id,
        f"Apakah nomor anda sudah benar?\n`{nomor}`",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["confirm_y", "confirm_x"])
def confirm_step(call):
    if call.data == "confirm_x":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message_id,
            text="Proses dibatalkan. /badakin lagi kalo mau ngulang 😂"
        )
        return

    # Lanjut ke animasi
    nomor = user_data[call.from_user.id]['nomor']
    run_fake_hack(call.message, nomor)

def run_fake_hack(message, nomor):
    logs = [
        "Menginisialisasi modul BADAK...",
        "Melewati firewall WhatsApp LLC...",
        "Mendekripsi hash nomor...",
        "Menyuntikkan buff Dewa WA...",
        "Mengoptimalkan sinyal 6G...",
        "Membypass limit Meta..."
    ]

    # Edit pesan konfirmasi jadi animasi
    for i in range(11):
        percent = i * 10
        bar = '█' * i + '>' + '─' * (10 - i)
        if i == 10: bar = '█' * 10

        log = random.choice(logs) if i < 10 else "Proses Selesai"
        text = f"`[SYSTEM] {log}`\n`[{bar}] {percent}%`"
        
        bot.edit_message_text(text, chat_id=message.chat.id, message_id=message.message_id, parse_mode='Markdown')
        time.sleep(random.uniform(0.2, 0.5))

    # Hasil Akhir
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
    bot.edit_message_text(hasil, chat_id=message.chat.id, message_id=message.message_id, parse_mode='Markdown')

if __name__ == '__main__':
    print("Bot BADAKIN WA Jalan di Railway...")
    bot.polling(none_stop=True)
