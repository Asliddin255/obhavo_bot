from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup as BS

t = requests.get('https://sinoptik.ua/погода-чиназ')
html_t = BS(t.content, 'html.parser')

for el in html_t.select('.EGYIdMfE'):
    min = el.select('.cFBF0wTW')[0].text
    max = el.select('.cFBF0wTW')[1].text
    t_min = min[4:]
    t_max = max[5:]
    print(t_min, t_max)

def city():
    return [
        [InlineKeyboardButton("Yallama", callback_data=f"01")]
    ]


def back():
    return [
        [InlineKeyboardButton("Orqaga", callback_data=f"back1")]
    ]


# Inline tugmalarni boshqarish
def inline_hendlar(update, context):
    query = update.callback_query
    data = query.data.split("_")

    if data[0] == "01":
        query.message.edit_text(
            f"Bugun Yallama qishlog'ida havo o'zgarib turadi\n Kechasi: {t_min} 🌒\n Kunduzi: {t_max} 🌞"
            f"\nbo'lishi kutilmoqda 🌦",
            reply_markup=InlineKeyboardMarkup(back())
        )

    elif data[0] == "back1":
        query.message.edit_text(
            "Bu yerdan kerakli shaharni tanlang 👇",
            reply_markup=InlineKeyboardMarkup(city())
        )


# /start komandasi
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"Salom, {user.first_name} \nBu yerdan kerakli shaharni tanlang👇",
        reply_markup=InlineKeyboardMarkup(city())
    )


# Asosiy bot funksiyasi
def main():
    Token = "7377343432:AAF32YFP1Y_gZFUAgStrEUSVbOT9aGFpJqs"  # Tokenni o'rnating (originalingizni quying)
    updater = Updater(Token)

    # /start uchun handler
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Inline tugmalar uchun handler
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_hendlar))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
