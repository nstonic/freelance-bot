import os

import telebot
from dotenv import load_dotenv

import markups
import messages

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'], parse_mode=None)


@bot.message_handler(commands=['find_orders'])
def show_orders(message):
    """Выводим список 5 случайных свободных заказов"""
    pass


@bot.message_handler(commands=['new_orders'])
def show_orders(message):
    """Создаем новый заказ"""
    pass


@bot.message_handler(commands=['my_orders'])
def show_orders(message):
    """Выводим список заказов"""
    pass


@bot.message_handler(commands=['register'])
def send_welcome(message):
    """Предлагаем зарегистрироваться в роли исполнителя или заказчика"""
    bot.reply_to(message,
                 messages.REGISTER,
                 reply_markup=markups.choose_roll)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Выводим приветствие и список возможны запросов"""
    bot.reply_to(message,
                 messages.HELP.format(message.chat.first_name))


@bot.callback_query_handler(func=lambda call: call.data == 'roll_client')
def register_client(message):
    """Регистрируем клиента в базе"""
    pass


@bot.callback_query_handler(func=lambda call: call.data == 'roll_freelancer')
def register_client(message):
    """Регистрируем заказчика в базе"""
    pass


if __name__ == '__main__':
    bot.infinity_polling()
