import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

TOKEN = "8811219437:AAFpG02SWePgkcxBSRviE0zmb64qx0-nBDs"
ADMIN_ID =8242975077

bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

users_balance = {}

def get_balance(user_id):
    if user_id not in users_balance:
        users_balance[user_id] = 0
    return users_balance[user_id]

def main_menu():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("📥 شحن رصيد", "📤 سحب رصيد")
    markup.row("🎡 عجلة الحظ")
    markup.row("🎁 اهداء رصيد", "🎟 كود هدية")
    markup.row("💬 رسالة للادمن", "📞 تواصل معنا")
    markup.row("📜 السجل", "📝 الشروحات")
    markup.row("💰 نظام الاحالات")
    markup.row("👑 الجاكبوت", "⚠️ الشروط والاحكام")
    markup.row("🎯 توقع مجانا واربح")

    return markup

@bot.message_handler(commands=['start'])
def start(message):

    balance = get_balance(message.from_user.id)

    bot.send_message(
        message.chat.id,
        f"💰 رصيدك: {balance}",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def buttons(message):

    user_id = message.from_user.id

    if message.text == "🎡 عجلة الحظ":

        prize = random.choice([1,2,5,10])

        users_balance[user_id] += prize

        bot.send_message(
            message.chat.id,
            f"🎉 ربحت {prize}"
        )

    else:

        bot.send_message(
            message.chat.id,
            f"✅ اخترت {message.text}"
        )

keep_alive()

print("BOT RUNNING")

bot.infinity_polling(timeout=30, long_polling_timeout=30)
