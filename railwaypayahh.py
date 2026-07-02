import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) 

# === SETTING WAJIB JOIN ===
GROUP_ID = -1003574311686 
CHANNEL_ID = -1003515213121 
GROUP_LINK = "https://t.me/publicdanzztfr" # Ganti
CHANNEL_LINK = "https://t.me/privatallinformationdanz" # Ganti

def box(text):
    text = str(text).replace("&", "&amp;")
    return f"<blockquote><pre>{text}</pre></blockquote>"

def safe_edit(chat_id, msg_id, text):
    try:
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, parse_mode="HTML")
        return True
    except:
        return False

def check_membership(user_id):
    try:
        member_group = bot.get_chat_member(GROUP_ID, user_id).status
        member_channel = bot.get_chat_member(CHANNEL_ID, user_id).status
        return member_group not in ['left', 'kicked'] and member_channel not in ['left', 'kicked']
    except:
        return False 

@bot.message_handler(commands=['start', 'badakin'])
def start_cmd(message):
    user_id = message.from_user.id

    if not check_membership(user_id):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("JOIN GB1", url=GROUP_LINK),
            InlineKeyboardButton("JOIN CHANNEL", url=CHANNEL_LINK)
        )
        markup.add(
            InlineKeyboardButton("VERIFIKASI JOIN", callback_data="recheck")
        )
        
        bot.send_message(
            message.chat.id, 
            box("<b>AKSES DITOLAK ❌</b>\nWajib join Grup + Channel dulu.\n\nKlik tombol di bawah, lalu VERIFIKASI."), 
            reply_markup=markup, 
            parse_mode="HTML"
        )
        return

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("MULAI", callback_data="start_badak"))
    bot.send_message(message.chat.id, box("<b>PANEL BADAK V12.1</b>\nTekan MULAI"), reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
def all_callbacks(call):
    if not call.message: return
    try: bot.answer_callback_query(call.id)
    except: pass 
    msg_id = call.message.id

    if call.data == "recheck":
        start_cmd(call.message) # Cek ulang join

    elif call.data == "start_badak":
        sent = bot.send_message(call.message.chat.id, box("<b>INPUT TARGET:</b> +62..."), parse_mode="HTML")
        bot.register_next_step_handler(sent, get_number_step)

    elif call.data == "x":
        safe_edit(call.message.chat.id, msg_id, box("<b>DIBATALKAN</b>"))

    elif call.data.startswith("y|"):
        nomor = call.data.split("|", 1)[1]
        run_process(call.message.chat.id, msg_id, nomor)

def get_number_step(message):
    nomor = message.text.strip().replace(" ", "")
    if not nomor.startswith(('+62', '62')):
        bot.reply_to(message, box("<b>ERROR:</b> FORMAT NOMOR SALAH"), parse_mode="HTML")
        return
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Y", callback_data=f"y|{nomor}"), InlineKeyboardButton("X", callback_data="x"))
    bot.send_message(message.chat.id, box(f"<b>CEK TARGET:</b>\n{nomor}\n\nLANJUT?"), reply_markup=markup, parse_mode="HTML")

def run_process(chat_id, msg_id, nomor):
    for i in range(5):
        safe_edit(chat_id, msg_id, box(f"PROSES... {i*25}%"))
        time.sleep(0.7)
    
    # INI RESULT NYA. UDAH ADA <b>
    hasil = f"""<b>=== RESLUT ===</b>
<b>TARGET</b> : {nomor}
<b>STATUS</b> : SUCCESS✅
<b>SISTEM</b> : SUPER VIP BADAK✅
<b>FILE</b> : BADAK V2 DANZZ✅
================
<b>Lakukan :</b>

-> DIAMKAN WHATSAPP SELAMA
24 JAM
-> AKTIFKAN PROXY DENGAN
KODE 1.1.1.1
-> DIAMKAN LAGI SELAMA 6-7
HARI (LEBIH LAMA LEBIH
MANTAP)
-DI HARI KE 7 PUTUSKAN PROXY
DIAMKAN SELAMA 5 JAM
-> LANGSUNG DEH BUAT BLAST /
GARAP FILE✅"""
    safe_edit(chat_id, msg_id, box(hasil))

if __name__ == '__main__':
    print("Bot V11.1 ON")
    bot.infinity_polling(skip_pending=True)
