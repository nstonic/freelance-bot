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


@bot.message_handler(commands=['new_order'])
def show_orders(message):
    """Создаем новый заказ"""
    pass


@bot.message_handler(commands=['my_orders'])
def show_orders(message):
    """Выводим список заказов"""
    bot.reply_to(message,
                 messages.MY_ORDERS,
                 reply_markup=markups.my_orders)


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
def register_client(call):
    """Регистрируем клиента в базе"""
    bot.answer_callback_query(call.id, text=messages.REGISTER_OK)


@bot.callback_query_handler(func=lambda call: call.data == 'roll_freelancer')
def register_client(call):
    """Регистрируем заказчика в базе"""
    bot.answer_callback_query(call.id, text=messages.REGISTER_OK)


@bot.callback_query_handler(func=lambda call: 'order_' in call.data)
def register_client(call):
    """Отображаем информацию по заказу"""
    bot.answer_callback_query(call.id, text='ваш заказ')


if __name__ == '__main__':
    bot.infinity_polling()
