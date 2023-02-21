import datetime
import os
import re
from datetime import date

import telebot
from telebot.types import Message, CallbackQuery
from dotenv import load_dotenv

import db_client
import markups
import messages
import models

load_dotenv()
bot = telebot.TeleBot(os.environ['BOT_TOKEN'], parse_mode=None)


#  ********************  Общее  ********************  #

@bot.message_handler(commands=['start'])
def start(message: Message):
    """Выводит предложение зарегистрироваться"""

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
def show_main_menu(message: Message):
    """Выводит основное меню"""

    user_role = db_client.who_is_it(message.chat.id)
    if user_role == 'client':
        text = 'Основное меню'
        markup = markups.make_menu_from_list(['Создать тикет', 'Мои тикеты'])
    elif user_role == 'freelancer':
        text = 'Основное меню'
        markup = markups.make_menu_from_list(['Найти заказ', 'Заказы в работе'])
    else:
        text = messages.MENU_IS_NOT_ALLOWED
        markup = None
    bot.send_message(message.chat.id,
                     reply_markup=markup,
                     text=text)


@bot.callback_query_handler(func=lambda call: call.data in ['register_client', 'register_freelancer'])
def register_user(call: CallbackQuery):
    """Регистрирует пользователя в базе"""

    if db_client.register_user(call.from_user.id, role=call.data.lstrip('register_')):
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, text=messages.REGISTER_FALSE)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ticket_'))
def show_ticket_info(call: CallbackQuery):
    """Отображает информацию по тикету"""

    ticket_id = int(call.data.lstrip('ticket_'))
    ticket = db_client.show_ticket(ticket_id)

    ticket['status'] = messages.TICKET_STATUSES[ticket['status']]
    ticket['created_at'] = ticket['created_at'].strftime('%Y.%m.%d %H:%M:%S')
    if ticket['estimate_time']:
        ticket['estimate_time'] = ticket['estimate_time'].strftime('%Y.%m.%d')
    else:
        ticket['estimate_time'] = 'отсутствует'

    user_role = db_client.who_is_it(call.message.chat.id)
    buttons = {}
    if user_role == 'client':
        if ticket['status'] == messages.TICKET_STATUSES['waiting']:
            buttons['Удалить тикет'] = f'delete_ticket_{ticket_id}'
        else:
            buttons['Чат'] = f'start_chat_order_{ticket["order_id"]}'

    if user_role == 'freelancer':
        buttons = {'Взять в работу': f'take_ticket_{ticket_id}'}

    ticket_inline_markup = markups.make_inline_markups_from_dict(buttons)
    bot.answer_callback_query(call.id, text=messages.TICKET.format(ticket['status']))
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.TICKET_INFO.format(**ticket),
                     reply_markup=ticket_inline_markup,
                     parse_mode='HTML')


#  ********************  Сторона клиента  ********************  #

@bot.message_handler(regexp='Мои тикеты')
def show_client_tickets(message: Message):
    """Выводит список тикетов заказчика"""

    user_id = message.chat.id
    if db_client.who_is_it(user_id) != 'client':
        start(message)
        return
    if tickets := db_client.show_tickets(user_id):
        bot.send_message(
            user_id,
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
def create_new_ticket(message: Message):
    """Создаёт новый тикет"""

    user = db_client.who_is_it(message.from_user.id)
    if user == 'client':
        bot.send_message(
            message.chat.id,
            text=messages.INPUT_TITLE,
            reply_markup=markups.get_back_main_menu()
        )
        bot.register_next_step_handler(message,
                                       get_title)
    elif user == 'freelancer':
        bot.send_message(message.chat.id, text=messages.CREATING_IS_NOT_ALLOWED)
    else:
        start(message)


def get_title(message: Message):
    """Принимает от заказчика название тикета"""

    if message.text == 'Назад':
        show_main_menu(message)
        return
    if message.text == 'Основное меню':
        show_main_menu(message)
        return

    input_title = message.text
    client_id = message.chat.id
    client_tickets = db_client.show_tickets(client_id)
    ticket_titles = [ticket.title for ticket in client_tickets]

    if input_title in ticket_titles:
        bot.send_message(client_id, text=messages.TITLE_EXIST)
        bot.register_next_step_handler(message, get_title)
        return
    elif len(input_title) <= 30:
        ticket = dict(title=input_title)
    else:
        bot.send_message(client_id, text=messages.TITLE_LEN_ERROR)
        bot.register_next_step_handler(message, get_title)
        return
    bot.send_message(
        client_id,
        text=messages.INPUT_TICKET_TEXT,
        reply_markup=markups.get_back_main_menu()
    )
    bot.register_next_step_handler(message, get_text, ticket=ticket)


def get_text(message: Message, ticket: dict):
    """Принимает от заказчика текст тикета"""

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
    show_main_menu(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_ticket_'))
def delete_ticket(call: CallbackQuery):
    """Удаляет тикет"""

    ticket_id = int(call.data.lstrip('delete_ticket_'))
    ticket = db_client.show_ticket(ticket_id)
    if not ticket['order_id']:
        if db_client.delete_ticket(ticket_id):
            bot.answer_callback_query(call.id, text=messages.TICKET_DELETED)
            show_client_tickets(call.message)
        else:
            bot.answer_callback_query(messages.ERROR_500)
    else:
        bot.answer_callback_query(call.id, text=messages.CANT_DELETE)


#  ********************  Сторона фрилансера  ********************  #

@bot.message_handler(regexp='Найти заказ')
def find_tickets(message: Message):
    """Выводит список 5 случайных свободных тикетов"""

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
def show_freelancer_orders(message: Message):
    """Выводит список активных заказов фрилансера"""

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
def show_order_info(call: CallbackQuery):
    """Отображает информацию по заказу"""

    order_id = int(call.data.lstrip('order_'))
    order = db_client.show_order(order_id)
    order['status'] = messages.ORDER_STATUSES[order['status']]
    order['started_at'] = order['started_at'].strftime('%Y.%m.%d %H:%M:%S')
    order['estimate_time'] = order['estimate_time'].strftime('%Y.%m.%d')

    order_inline_markup = markups.get_order_buttons(order_id)

    bot.answer_callback_query(call.id, text='Ваш заказ')
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.ORDER_INFO.format(**order),
                     parse_mode='HTML',
                     reply_markup=order_inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('take_ticket_'))
def take_ticket(call: CallbackQuery):
    """Исполнитель берет тикет в работу"""

    ticket_id = int(call.data.lstrip('take_ticket_'))
    bot.register_next_step_handler(call.message,
                                   get_estimate_time,
                                   ticket_id=ticket_id,
                                   call=call)
    bot.send_message(call.message.chat.id,
                     text=messages.SET_EST_TIME,
                     reply_markup=markups.get_back_main_menu())


def get_estimate_time(message: Message, call: CallbackQuery, ticket_id: int):
    """Принимает оценочное время исполнения заказа"""

    if message.text == 'Назад':
        show_freelancer_orders(message)
        return
    if message.text == 'Основное меню':
        show_main_menu(message)
        return

    chat_id = message.chat.id
    message_text = message.text
    wrong_date = False
    if re.fullmatch(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d', message_text):
        splited_date = tuple(re.split(r'-|/|\.| ', message_text))
        try:
            est_date = datetime.date(*map(int, splited_date[::-1]))
        except ValueError:
            wrong_date = True
    else:
        wrong_date = True

    if wrong_date:
        bot.send_message(chat_id, messages.INVALID_DATE)
        take_ticket(call)
        return

    if est_date < date.today():
        bot.send_message(chat_id, messages.WRONG_DATE)
        take_ticket(call)
        return

    order_id = db_client.start_work(
        ticket_id=ticket_id,
        telegram_id=chat_id,
        estimate_time=est_date
    )
    order = db_client.show_order(order_id)
    send_notice(
        order_id=order_id,
        notice=messages.TICKET_TAKEN.format(order['title']),
        sender_id=chat_id
    )
    show_freelancer_orders(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('close_order_'))
def close_order(call: CallbackQuery):
    """Исполнитель закрывает заказ"""

    order_id = int(call.data.lstrip('close_order_'))
    order = db_client.show_order(order_id)
    if db_client.close_order(order_id):
        bot.answer_callback_query(call.id, text=messages.CLOSED)
        send_notice(order_id=order_id,
                    notice=messages.TICKET_CLOSED.format(order['title']),
                    sender_id=call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, text=messages.ERROR_500)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel_order_'))
def cancel_order(call: CallbackQuery):
    """Исполнитель отказывается от заказа"""

    order_id = int(call.data.lstrip('cancel_order_'))
    order = db_client.show_order(order_id)
    if db_client.cancel_order(order_id):
        bot.answer_callback_query(call.id, text=messages.CANCELED)
        send_notice(order_id=order_id,
                    notice=messages.TICKET_CANCELED.format(order['title']),
                    sender_id=call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, text=messages.ERROR_500)


#  ********************  Чат  ********************  #

@bot.callback_query_handler(func=lambda call: call.data.startswith('start_chat_order_'))
def go_to_chat_mode(call: CallbackQuery):
    """Переводит бота в режим чата между сторонами заказа."""

    bot.clear_step_handler(call.message)
    chat_markup = markups.make_menu_from_list(['Выйти из чата', 'История чата'])
    bot.send_message(
        chat_id=call.message.chat.id,
        text=messages.SEND_MESSAGE,
        reply_markup=chat_markup
    )
    bot.register_next_step_handler(
        call.message,
        send_message_to_chat,
        order_id=int(call.data.lstrip('start_chat_order_'))
    )


def send_message_to_chat(message: Message, order_id: int):
    """Принимает сообщение от пользователя, записывает его в историю чата
     и отправляет уведомление собеседнику"""

    if message.text == 'Выйти из чата':
        bot.clear_step_handler(message)
        show_main_menu(message)
        return
    if message.text == 'История чата':
        show_chat_history(message, order_id)
        return

    user_id = message.chat.id
    msg_text = message.text

    db_client.create_chat_msg(
        telegram_id=user_id,
        message_text=msg_text,
        order_id=order_id
    )

    bot.clear_step_handler(message)
    notice = f'{messages.INCOMING}\n\n{msg_text}'
    send_notice(order_id=order_id, notice=notice, sender_id=user_id)
    bot.register_next_step_handler(
        message,
        send_message_to_chat,
        order_id=order_id
    )


def show_chat_history(message: Message, order_id: int):
    """Показывает пользователю историю чата по данному заказу"""
    order = db_client.show_order(order_id)
    chat = db_client.show_chat(order_id)
    bot.clear_step_handler(message)
    bot.send_message(
        chat_id=message.chat.id,
        text=compile_whole_chat_in_one_msg(order['title'], chat)
    )
    bot.register_next_step_handler(
        message,
        send_message_to_chat,
        order_id=order_id
    )


def compile_whole_chat_in_one_msg(order_title: str, chat: list[dict]) -> str:
    """Компилирует весь чат по данному заказу в одно сообщение, форматированное в следующем виде:

        История чата по заказу "Название заказа":

        YYYY-MM-DD HH:MM:SS:  [Роль пользователя]
        [текст сообщения]

        YYYY-MM-DD HH:MM:SS:  [Роль пользователя]
        [текст сообщения]

        и т.д.
    """

    roles = {'client': 'Заказчик', 'freelancer': 'Исполнитель'}
    if chat:
        compiled_messages = [f'{msg["sending_at"].replace(microsecond=0)}:  {roles[msg["user_role"]]}\n{msg["text"]}'
                             for msg in chat]
        chat_text = '\n\n'.join(compiled_messages)
    else:
        chat_text = messages.NO_MESSAGES
    return f'История чата по заказу "{order_title}":\n\n{chat_text}'


def send_notice(order_id: int, notice: str, sender_id: int):
    """Отправляем оповещение другой стороне"""

    sender_role = db_client.who_is_it(sender_id)
    receiver_role = {'client': 'freelancer', 'freelancer': 'client'}[sender_role]
    order = db_client.show_order(order_id)
    receiver_id = order[receiver_role]
    order_or_ticket = {'client': 'тикету', 'freelancer': 'заказу'}[receiver_role]
    format_values = dict(
        order_or_ticket=order_or_ticket,
        title=order['title']
    )

    notice_markup = markups.get_notice_buttons(
        user_role=receiver_role,
        order_id=order_id,
        ticket_id=order['ticket_id']
    )
    bot.send_message(
        receiver_id,
        notice.format(**format_values),
        parse_mode='HTML',
        reply_markup=notice_markup
    )


if __name__ == '__main__':
    if not os.path.isfile(os.environ['DATABASE_PATH']):
        models.create_tables()
    bot.infinity_polling()
