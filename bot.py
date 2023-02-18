import os
from datetime import date

import telebot
from dotenv import load_dotenv

import db_client
import markups
import messages
import models

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'], parse_mode=None)


#  ********************  Общее  ********************  #

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    """Выводим приветствие и предложение зарегистрироваться"""
    if not db_client.who_is_it(message.from_user.id):
        register_markup = markups.make_inline_markups_from_dict(
            {'Заказчик': 'register_client',
             'Исполнитель': 'register_freelancer'}
        )
        bot.send_message(message.chat.id,
                         messages.CHOOSE_ROLE,
                         reply_markup=register_markup)
    else:
        show_main_menu(message)


@bot.message_handler(regexp='Основное меню')
@bot.message_handler(commands=['main_menu'])
def show_main_menu(message: telebot.types.Message):
    """Выводим основное меню"""
    user_role = db_client.who_is_it(message.chat.id)
    if user_role == 'client':
        text = 'Меню заказчика'
        markup = markups.make_menu_from_list(['Создать тикет', 'Мои тикеты'])
    elif user_role == 'freelancer':
        text = 'Меню исполнителя'
        markup = markups.make_menu_from_list(['Найти заказ', 'Заказы в работе'])
    else:
        text = messages.MENU_IS_NOT_ALLOWED
        markup = None
    bot.send_message(message.chat.id,
                     reply_markup=markup,
                     text=text)


@bot.callback_query_handler(func=lambda call: call.data in ['register_client', 'register_freelancer'])
def register_user(call: telebot.types.CallbackQuery):
    """Регистрируем пользователя в базе"""

    if db_client.register_user(call.from_user.id, role=call.data.lstrip('register_')):
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, text=messages.REGISTER_FALSE)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ticket_'))
def show_ticket_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по тикету"""
    ticket_id = int(call.data.lstrip('ticket_'))
    ticket = db_client.show_ticket(ticket_id)
    ticket['status'] = messages.TICKET_STATUSES[ticket['status']]
    user_role = db_client.who_is_it(call.message.chat.id)
    buttons = {}
    if user_role == 'client':
        buttons['Удалить тикет'] = f'delete_ticket_{ticket_id}'
        if ticket['status'] != messages.TICKET_STATUSES['waiting']:
            buttons['Чат'] = f'show_chat_order_{ticket["order_id"]}'
    if user_role == 'freelancer':
        buttons = {'Взять в работу': f'take_ticket_{ticket_id}'}

    ticket_inline_markup = markups.make_inline_markups_from_dict(buttons)
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.TICKET_INFO.format(**ticket),
                     reply_markup=ticket_inline_markup,
                     parse_mode='HTML')


#  ********************  Сторона клиента  ********************  #

@bot.message_handler(regexp='Мои тикеты')
def show_client_tickets(message: telebot.types.Message):
    """Выводим список тикетов клиента"""
    if db_client.who_is_it(message.chat.id) != 'client':
        start(message)
        return
    if tickets := db_client.find_tickets():
        bot.send_message(
            message.chat.id,
            messages.MY_TICKETS,
            reply_markup=markups.make_inline_markups_from_dict(
                {ticket.title: f'ticket_{ticket.get_id()}'
                 for ticket in tickets},
                row_width=1
            )
        )
    else:
        bot.send_message(message.chat.id, messages.NO_TICKETS)


@bot.message_handler(regexp='Создать тикет')
def create_new_ticket(message: telebot.types.Message):
    """Создаем новый тикет"""
    user = db_client.who_is_it(message.from_user.id)
    if user == 'client':
        bot.send_message(
            message.chat.id,
            text=messages.INPUT_TITLE,
            reply_markup=markups.make_menu_from_list(['Создать тикет', 'Мои тикеты'])
        )
        bot.register_next_step_handler(message,
                                       get_title)
    elif user == 'freelancer':
        bot.send_message(message.chat.id, text=messages.CREATING_IS_NOT_ALLOWED)
    else:
        start(message)


def get_title(message: telebot.types.Message):
    """Получаем от клиента название тикета"""
    if message.text == 'Назад':
        create_new_ticket(message)
        return
    if message.text == 'Основное меню':
        show_main_menu(message)
        return

    if len(message.text) <= 30:
        ticket = dict(title=message.text)
    else:
        bot.send_message(message.chat.id, text=messages.TITLE_ERROR)
        bot.register_next_step_handler(message, get_title)
        return
    bot.send_message(
        message.chat.id,
        text=messages.INPUT_TICKET_TEXT,
        reply_markup=markups.get_back_main_menu()
    )
    bot.register_next_step_handler(message, get_text, ticket=ticket)


def get_text(message: telebot.types.Message, ticket: dict):
    """Получаем от клиента текст тикета"""
    if message.text == 'Назад':
        create_new_ticket(message)
        return
    if message.text == 'Основное меню':
        show_main_menu(message)
        return

    ticket['text'] = message.text
    bot.send_message(message.chat.id,
                     text=messages.TICKET_CREATED.format(**ticket),
                     parse_mode='HTML')
    db_client.create_ticket(message.chat.id, **ticket)
    show_client_tickets(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_ticket_'))
def delete_ticket(call: telebot.types.CallbackQuery):
    """Удаляем тикет"""
    ticket_id = int(call.data.lstrip('delete_ticket_'))
    if db_client.delete_ticket(ticket_id):
        bot.answer_callback_query(call.id, text=messages.TICKET_DELETED)
        show_client_tickets(call.message)
    else:
        bot.answer_callback_query(messages.ERROR_500)


#  ********************  Сторона фрилансера  ********************  #

@bot.message_handler(regexp='Найти заказ')
def find_tickets(message: telebot.types.Message):
    """Выводим список 5 случайных свободных заказов"""
    user = db_client.who_is_it(message.from_user.id)
    if user == 'freelancer':
        tickets = db_client.find_tickets()
        markup = markups.make_inline_markups_from_dict(
            {ticket.title: f'ticket_{ticket.get_id()}'
             for ticket in tickets},
            row_width=1
        )
        text = messages.TICKET_CHOICE if tickets else messages.NO_ACTIVE_TICKETS
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif user == 'client':
        bot.send_message(message.chat.id, text=messages.SEARCHING_IS_NOT_ALLOWED)
    else:
        start(message)


@bot.message_handler(regexp='Заказы в работе')
def show_freelancer_orders(message: telebot.types.Message):
    """Выводим список заказов фрилансера"""
    if orders := db_client.show_my_orders(message.chat.id):
        bot.send_message(
            message.chat.id,
            messages.MY_ORDERS,
            reply_markup=markups.make_inline_markups_from_dict(
                {order.ticket.title: f'order_{order.get_id()}'
                 for order in orders},
                row_width=1
            )
        )
    else:
        bot.send_message(message.chat.id, messages.NO_ORDERS)


@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def show_order_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по заказу"""
    order_id = int(call.data.lstrip('order_'))
    order = db_client.show_order(order_id)
    order['status'] = messages.ORDER_STATUSES[order['status']]
    order_inline_markup = markups.get_order_buttons(order_id)

    bot.answer_callback_query(call.id, text='Ваш заказ')
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.ORDER_INFO.format(**order),
                     parse_mode='HTML',
                     reply_markup=order_inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('take_ticket_'))
def take_ticket(call: telebot.types.CallbackQuery):
    """Фрилансер берет тикет в работу"""
    ticket_id = int(call.data.lstrip('take_ticket_'))
    bot.register_next_step_handler(call.message,
                                   get_estimate_time,
                                   ticket_id=ticket_id,
                                   call=call)
    bot.send_message(call.message.chat.id,
                     text=messages.SET_EST_TIME,
                     reply_markup=markups.get_back_main_menu())


def get_estimate_time(message: telebot.types.Message,
                      call: telebot.types.CallbackQuery,
                      ticket_id: int):
    """Запрашиваем оценочное время исполнения"""
    if message.text == 'Назад':
        show_freelancer_orders(message)
        return
    if message.text == 'Основное меню':
        show_main_menu(message)
        return

    try:
        est_time = date.fromisoformat(message.text).strftime("%d/%m/%Y, %H:%M")
    except ValueError:
        bot.send_message(message.chat.id, messages.INVALID_DATE)
        take_ticket(call)
        return

    db_client.start_work(ticket_id=ticket_id,
                         telegram_id=message.chat.id,
                         estimate_time=est_time)
    show_freelancer_orders(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('close_order_'))
def close_order(call: telebot.types.CallbackQuery):
    order_id = int(call.data.lstrip('close_order_'))
    if db_client.close_order(order_id):
        bot.answer_callback_query(call.id, text=messages.ORDER_CLOSED)
    else:
        bot.answer_callback_query(call.id, text=messages.ERROR_500)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel_order_'))
def cancel_order(call: telebot.types.CallbackQuery):
    order_id = int(call.data.lstrip('cancel_order_'))
    if db_client.cancel_order(order_id):
        bot.answer_callback_query(call.id, text=messages.ORDER_CANCELED)
    else:
        bot.answer_callback_query(call.id, text=messages.ERROR_500)


#  ********************  Чат  ********************  #

@bot.callback_query_handler(func=lambda call: call.data.startswith('show_chat_order_'))
def show_chat(call: telebot.types.CallbackQuery):
    """Показываем чат"""
    order_id = int(call.data.lstrip('show_chat_order_'))
    chat = db_client.show_chat(order_id) or messages.NO_MESSAGE
    bot.send_message(chat_id=call.message.chat.id,
                     text=chat)
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.SEND_MESSAGE,
                     reply_markup=markups.get_back_main_menu())
    bot.register_next_step_handler(call.message,
                                   get_chat_message,
                                   call=call,
                                   order_id=order_id)


def get_chat_message(message: telebot.types.Message,
                     call: telebot.types.CallbackQuery,
                     order_id: int):
    """Принимаем сообщение в чат"""
    if message.text == 'Назад':
        call.data = call.data.lstrip('show_chat_')
        show_order_info(call)
        return
    if message.text == 'Основное меню':
        show_main_menu(message)
        return

    if db_client.get_chat_msg(user_role=db_client.who_is_it(message.chat.id),
                              message_text=message.text,
                              order_id=order_id):
        bot.answer_callback_query(call.id, messages.MESSAGE_SEND)
        send_chat_message(order_id, message)
    else:
        bot.answer_callback_query(call.id, messages.ERROR_500)
        call.data = call.data.lstrip('show_chat_')
        show_order_info(call)


def send_chat_message(order_id: int, message: telebot.types.Message):
    """Пересылаем сообщение другой стороне"""
    user_role = db_client.who_is_it(message.chat.id)
    receiver = {'client': 'freelancer', 'freelancer': 'client'}[user_role]
    order = db_client.show_order(order_id)
    receiver_id = order[receiver]
    format_values = dict(
        order_or_ticket={'client': 'заказу', 'freelancer': 'тикету'}[user_role],
        title=order['title'],
        text=message.text
    )
    chat_markup = markups.make_inline_markups_from_dict({'Чат': f'show_chat_order_{order_id}'})
    bot.send_message(receiver_id,
                     messages.INCOMING.format(**format_values),
                     reply_markup=chat_markup)


if __name__ == '__main__':
    if not os.path.isfile(os.environ['DATABASE_PATH']):
        models.create_tables()
    bot.infinity_polling()
