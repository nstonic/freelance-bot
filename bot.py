import os

import telebot
from dotenv import load_dotenv

import db_client
import markups
import messages
import models

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'], parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    """Выводим приветствие и предложение зарегистрироваться"""
    if not db_client.who_is_it(message.from_user.id):
        bot.send_message(message.chat.id,
                         messages.START.format(message.chat.first_name),
                         reply_markup=markups.register())
    else:
        show_main_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == 'register')
def register(call: telebot.types.CallbackQuery):
    """Предлагаем зарегистрироваться в роли исполнителя или заказчика"""
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    bot.send_message(call.message.chat.id,
                     messages.REGISTER,
                     reply_markup=markups.choose_roll())


@bot.callback_query_handler(func=lambda call: call.data == 'roll_client')
def register_client(call: telebot.types.CallbackQuery):
    """Регистрируем клиента в базе"""
    if db_client.register_client(call.from_user.id):
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    show_main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'roll_freelancer')
def register_freelancer(call: telebot.types.CallbackQuery):
    """Регистрируем заказчика в базе"""
    if db_client.register_freelancer(call.from_user.id):
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    show_main_menu(call.message)


@bot.message_handler(commands=['menu'])
def show_main_menu(message: telebot.types.Message):
    """Выводим основное меню"""
    user = db_client.who_is_it(message.from_user.id)
    text = messages.HELLO.format(message.from_user.first_name)
    if user == 'client':
        bot.send_message(message.chat.id,
                         reply_markup=markups.get_client_menu(),
                         text=text)
    elif user == 'freelancer':
        bot.send_message(message.chat.id,
                         reply_markup=markups.get_freelancer_menu(),
                         text=text)
    else:
        start(message)


@bot.message_handler(regexp='Найти заказ')
def find_orders(message: telebot.types.Message):
    """Выводим список 5 случайных свободных заказов"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    user = db_client.who_is_it(message.from_user.id)
    if user == 'freelancer':
        pass
    elif user == 'client':
        bot.send_message(message.chat.id, text=messages.ONLY_FREELANCER_CAN_SEARCH_FOR_ORDERS)
    else:
        start(message)


@bot.message_handler(regexp='Создать тикет')
def create_new_ticket(message: telebot.types.Message):
    """Создаем новый тикет"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    user = db_client.who_is_it(message.from_user.id)
    if user == 'client':
        bot_message_id = bot.send_message(message.chat.id, text=messages.INPUT_TITLE).id
        bot.register_next_step_handler(message,
                                       get_title,
                                       bot_message_id=bot_message_id)
    elif user == 'freelancer':
        bot.send_message(message.chat.id, text=messages.ONLY_CLIENT_CAN_CREATE_ORDER)
    else:
        start(message)


def get_title(message: telebot.types.Message, bot_message_id: int):
    """Получаем от клиента название тикета"""
    ticket = dict(
        title=message.text
    )
    bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot_message_id = bot.send_message(message.chat.id, text=messages.INPUT_TICKET_TEXT).id
    bot.register_next_step_handler(message,
                                   get_text,
                                   ticket=ticket,
                                   bot_message_id=bot_message_id)


def get_text(message: telebot.types.Message, ticket: dict, bot_message_id: int):
    """Получаем от клиента текст тикета"""
    ticket['text'] = message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    bot.send_message(message.chat.id,
                     text=messages.TICKET_CREATED.format(ticket['title'], ['text']))


@bot.message_handler(regexp='Мои тикеты')
def show_client_tickets(message: telebot.types.Message):
    """Выводим список тикетов клиента"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id,
                     messages.MY_TICKETS,
                     reply_markup=markups.get_tickets_list())


@bot.callback_query_handler(func=lambda call: call.data.startswith('ticket_'))
def show_ticket_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по тикету"""
    bot.answer_callback_query(call.id, text='ваш тикет')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.message_handler(regexp='Заказы в работе')
def show_freelancer_orders(message: telebot.types.Message):
    """Выводим список заказов фрилансера"""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id,
                     messages.MY_ORDERS,
                     reply_markup=markups.get_orders_list())


@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def show_order_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по заказу"""
    bot.answer_callback_query(call.id, text='ваш заказ')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


if __name__ == '__main__':
    if not os.path.isfile(os.environ['DATABASE_PATH']):
        models.create_tables()
    bot.infinity_polling()
