import telebot
import os # TAMBAHIN INI
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN") # AMBIL DARI RAILWAY
bot = telebot.TeleBot(BOT_TOKEN)

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
    bot.answer_callback_query(call.id) # Biar loading tombolnya ilang
    bot.send_message( # GANTI JADI SEND_MESSAGE BIAR BISA NEXT STEP
        call.message.chat.id,
        "Silakan anda memasukkan nomor dengan awalan `+62` atau `62`\n\nContoh: `+628123456789`",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(call.message, get_number_step) # Sekarang ini valid

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
    bot.answer_callback_query(call.id)
    if call.data == "confirm_x":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message_id,
            text="Proses dibatalkan. /badakin lagi kalo mau ngulang 😂"
        )
        return

    nomor = user_data[call.from_user.id]['nomor']
    run_fake_hack(call, nomor) # KIRIM CALL BUKAN MESSAGE

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

    # DIBUAT LEBIH LAMBAT BIAR GAK KENA LIMIT RAILWAY
    for i in range(11):
        percent = i * 10
        bar = '█' * i + '>' + '─' * (10 - i)
        if i == 10: bar = '█' * 10

        log = random.choice(logs) if i < 10 else "Proses Selesai"
        text = f"`[SYSTEM] {log}`\n`[{bar}] {percent}%`"
        
        try:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=msg.message_id, parse_mode='Markdown')
        except telebot.apihelper.ApiTelegramException:
            pass # Gagal edit karena kecepetan, skip aja biar gak crash
        time.sleep(0.5) # TADI 0.2, INI 0.5 BIAR AMAN

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
    bot.infinity_polling(timeout=10, long_polling_timeout=5) # LEBIH STABIL DARI POLLING
