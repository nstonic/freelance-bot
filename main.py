import os

import telebot
from dotenv import load_dotenv

import markups

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'], parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_first_name = str(message.chat.first_name)
    bot.reply_to(message,
                 f"Здравствуй! {user_first_name}\nДобро пожаловать во ФрилансБот.\n"
                 f"В качестве кого ты хочешь зарегистрироваться?",
                 reply_markup=markups.choose_roll)


@bot.callback_query_handler(func=lambda call: call.data == 'roll_client')
def register_client(message):
    """Регистрируем клиента в базе"""
    pass


@bot.callback_query_handler(func=lambda call: call.data == 'roll_doer')
def register_client(message):
    """Регистрируем заказчика в базе"""
    pass


if __name__ == '__main__':
    bot.infinity_polling()
