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


@bot.message_handler(regexp='Найти заказ')
def find_tickets(message: telebot.types.Message):
    """Выводим список 5 случайных свободных заказов"""
    user = db_client.who_is_it(message.from_user.id)
    if user == 'freelancer':
        tickets = db_client.find_tickets()
        markup = markups.make_inline_markups_from_dict(
            {ticket.title:f'ticket_{ticket.get_id()}'
             for ticket in tickets}
        )
        text = messages.TICKET_CHOICE if tickets else messages.NO_ACTIVE_TICKETS
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif user == 'client':
        bot.send_message(message.chat.id, text=messages.SEARCHING_IS_NOT_ALLOWED)
    else:
        start(message)


@bot.message_handler(regexp='Создать тикет')
def create_new_ticket(message: telebot.types.Message):
    """Создаем новый тикет"""
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
    show_main_menu(message)


@bot.message_handler(regexp='Мои тикеты')
def show_client_tickets(message: telebot.types.Message):
    """Выводим список тикетов клиента"""
    if tickets := db_client.find_tickets():
        bot.send_message(
            message.chat.id,
            messages.MY_TICKETS,
            reply_markup=markups.make_inline_markups_from_dict(
                {ticket.title: f'ticket_{ticket.get_id()}'
                 for ticket in tickets}
            )
        )
    else:
        bot.send_message(message.chat.id, messages.NO_TICKETS)


@bot.message_handler(regexp='Заказы в работе')
def show_freelancer_orders(message: telebot.types.Message):
    """Выводим список заказов фрилансера"""
    if orders := db_client.show_my_orders(message.chat.id):
        bot.send_message(
            message.chat.id,
            messages.MY_ORDERS,
            reply_markup=markups.make_inline_markups_from_dict(
                {order.title: order.get_id()
                 for order in orders}
            )
        )
    else:
        bot.send_message(message.chat.id, messages.NO_ORDERS)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ticket_'))
def show_ticket_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по тикету"""
    ticket = db_client.show_ticket(int(call.data.lstrip('ticket_')))
    ticket_markup = None
    user_role = db_client.who_is_it(call.message.chat.id)

    if user_role == 'client':
        if ticket['status'] != messages.TICKET_STATUSES['waiting']:
            ticket_markup = markups.make_inline_markups_from_dict(
                {'Чат': 'show_chat',
                 'Удалить тикет': 'delete_ticket'}
            )
        else:
            ticket_markup = markups.make_inline_markups_from_dict(
                {'Удалить тикет': 'delete_ticket'}
            )

    if user_role == 'freelancer':
        if ticket['status'] == messages.TICKET_STATUSES['waiting']:
            ticket_markup = markups.make_inline_markups_from_dict(
                {'Взять в работу': 'take_ticket'}
            )
        else:
            ticket_markup = markups.make_inline_markups_from_dict(
                {'Чат': 'show_chat'}
            )

    bot.answer_callback_query(call.id, text=f'Информация по тикету {ticket["title"]}')
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.TICKET_INFO.format(**ticket),
                     reply_markup=ticket_markup,
                     parse_mode='HTML')
    delete_messages(chat_id=call.message.chat.id, mes_ids=[call.message.id])


@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def show_order_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по заказу"""

    # order = db_client.show_order(int(call.data.strip('order_')))
    order = {
        'title': 'Построить дом',
        'started_at': '17.02.23',
        'text': 'Из кирпича',
        'status': 'В работе',
        'client': 'Петя',
        'estimate_time': '17.02.24'
    }
    order_markup = markups.make_inline_markups_from_dict({'Отправить сообщение': 'send_mes_to_client',
                                                          'Читать переписку': 'show_chat',
                                                          'Изменить статус': 'change_status'})
    bot.answer_callback_query(call.id, text='Ваш заказ')
    bot.send_message(chat_id=call.message.chat.id,
                     text=messages.ORDER_INFO.format(**order),
                     parse_mode='HTML',
                     reply_markup=order_markup)
    delete_messages(chat_id=call.message.chat.id, mes_ids=[call.message.id])


def delete_messages(chat_id: int, mes_ids: list):
    for mes_id in mes_ids:
        try:
            bot.delete_message(chat_id=chat_id, message_id=mes_id)
        except telebot.apihelper.ApiTelegramException:
            pass


if __name__ == '__main__':
    if not os.path.isfile(os.environ['DATABASE_PATH']):
        models.create_tables()
    bot.infinity_polling()
