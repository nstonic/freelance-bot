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
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    match db_client.who_is_it(message.from_user.id):
        case 'freelancer':
            pass
        case 'client' | None:
            bot.send_message(message.chat.id, text=messages.ONLY_FREELANCER_CAN_SEARCH_FOR_ORDERS)


@bot.message_handler(commands=['new_order'])
def create_new_order(message: telebot.types.Message):
    """Создаем новый заказ"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    match db_client.who_is_it(message.from_user.id):
        case 'client':
            pass
        case 'freelancer' | None:
            bot.send_message(message.chat.id, text=messages.ONLY_CLIENT_CAN_CREATE_ORDER)


@bot.message_handler(commands=['my_orders'])
def show_user_orders(message: telebot.types.Message):
    """Выводим список заказов"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id,
                     messages.MY_ORDERS,
                     reply_markup=markups.my_orders)


@bot.message_handler(commands=['register'])
def register(message: telebot.types.Message):
    """Предлагаем зарегистрироваться в роли исполнителя или заказчика"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id,
                     messages.REGISTER,
                     reply_markup=markups.choose_roll)


@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message):
    """Выводим приветствие и список возможны запросов"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id, messages.HELP)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    """Выводим приветствие и список возможны запросов"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id,
                     messages.START.format(message.chat.first_name))


@bot.callback_query_handler(func=lambda call: call.data == 'roll_client')
def register_client(call: telebot.types.CallbackQuery):
    """Регистрируем клиента в базе"""
    if db_client.register_client(call.from_user.id):
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.callback_query_handler(func=lambda call: call.data == 'roll_freelancer')
def register_freelancer(call: telebot.types.CallbackQuery):
    """Регистрируем заказчика в базе"""
    if db_client.register_freelancer(call.from_user.id):
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def show_order_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по заказу"""
    bot.answer_callback_query(call.id, text='ваш заказ')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


if __name__ == '__main__':
    bot.infinity_polling()
