import os

import telebot
from dotenv import load_dotenv

import db_client
import markups
import messages

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'], parse_mode=None)


@bot.message_handler(commands=['find_order'])
def find_orders(message: telebot.types.Message):
    """Выводим список 5 случайных свободных заказов"""
    match db_client.who_is_it(message.from_user.id):
        case 'freelancer':
            pass
        case 'client' | None:
            bot.answer_callback_query(message.id, text=messages.ONLY_FREELANCER_CAN_SEARCH_FOR_ORDERS)


@bot.message_handler(commands=['new_order'])
def create_new_order(message: telebot.types.Message):
    """Создаем новый заказ"""
    match db_client.who_is_it(message.from_user.id):
        case 'client':
            pass
        case 'freelancer' | None:
            bot.answer_callback_query(message.id, text=messages.ONLY_CLIENT_CAN_CREATE_ORDER)


@bot.message_handler(commands=['my_orders'])
def show_user_orders(message: telebot.types.Message):
    """Выводим список заказов"""
    bot.reply_to(message,
                 messages.MY_ORDERS,
                 reply_markup=markups.my_orders)


@bot.message_handler(commands=['register'])
def register(message: telebot.types.Message):
    """Предлагаем зарегистрироваться в роли исполнителя или заказчика"""
    bot.reply_to(message,
                 messages.REGISTER,
                 reply_markup=markups.choose_roll)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    """Выводим приветствие и список возможны запросов"""
    bot.reply_to(message,
                 messages.HELP.format(message.chat.first_name))


@bot.callback_query_handler(func=lambda call: call.data == 'roll_client')
def register_client(message: telebot.types.Message):
    """Регистрируем клиента в базе"""
    if db_client.register_client(message.from_user.id):
        bot.answer_callback_query(message.id, text=messages.REGISTER_OK)


@bot.callback_query_handler(func=lambda call: call.data == 'roll_freelancer')
def register_freelancer(message: telebot.types.Message):
    """Регистрируем заказчика в базе"""
    if db_client.register_freelancer(message.from_user.id):
        bot.answer_callback_query(message.id, text=messages.REGISTER_OK)


@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def show_order_info(message: telebot.types.Message):
    """Отображаем информацию по заказу"""
    bot.answer_callback_query(message.id, text='ваш заказ')


if __name__ == '__main__':
    bot.infinity_polling()
