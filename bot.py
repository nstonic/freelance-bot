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
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id])
    if not db_client.who_is_it(message.from_user.id):
        start_markup = markups.make_inline_markups_from_dict({'Зарегистрироваться': 'choose_role',
                                                              'Справка': 'help'})
        bot.send_message(message.chat.id,
                         messages.START.format(message.chat.first_name),
                         reply_markup=start_markup)
    else:
        show_main_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def show_help(call: telebot.types.CallbackQuery):
    """Показываем справку"""
    delete_messages(chat_id=call.message.chat.id, mes_ids=[call.message.id])
    help_markup = markups.make_inline_markups_from_dict({'Зарегистрироваться': 'choose_role'})
    bot.send_message(call.message.chat.id,
                     messages.HELP,
                     reply_markup=help_markup)


@bot.message_handler(commands=['menu'])
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
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id])


@bot.callback_query_handler(func=lambda call: call.data == 'choose_role')
def choose_role(call: telebot.types.CallbackQuery):
    """Предлагаем зарегистрироваться в роли исполнителя или заказчика"""
    delete_messages(chat_id=call.message.chat.id, mes_ids=[call.message.id])
    register_markup = markups.make_inline_markups_from_dict({'Заказчик': 'register_client',
                                                             'Исполнитель': 'register_freelancer'})
    bot.send_message(call.message.chat.id,
                     messages.CHOOSE_ROLE,
                     reply_markup=register_markup)


@bot.callback_query_handler(func=lambda call: call.data in ['register_client', 'register_freelancer'])
def register_client(call: telebot.types.CallbackQuery):
    """Регистрируем пользователя в базе"""

    # if registered := db_client.register_user(call.from_user.id, role=call.data.strip(register_)):
    #     bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
    #     show_main_menu(call.message)
    # else:
    #     bot.answer_callback_query(call.id, text=messages.REGISTER_FALSE)
    # delete_messages(chat_id=call.message.chat.id, mes_ids=[call.message.id])

    """Временное решение"""
    registered = False

    if call.data == 'register_client':
        registered = db_client.register_client(call.from_user.id)
    elif call.data == 'register_freelancer':
        registered = db_client.register_freelancer(call.from_user.id)

    if registered:
        bot.answer_callback_query(call.id, text=messages.REGISTER_OK)
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, text=messages.REGISTER_FALSE)
    delete_messages(chat_id=call.message.chat.id, mes_ids=[call.message.id])


@bot.message_handler(regexp='Найти заказ')
def find_orders(message: telebot.types.Message):
    """Выводим список 5 случайных свободных заказов"""
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id])
    user = db_client.who_is_it(message.from_user.id)
    if user == 'freelancer':
        tickets = db_client.find_tickets()
        markup = markups.get_tickets_choose_btns(tickets)
        bot.send_message(message.chat.id, text=messages.TICKET_CHOICE, reply_markup=markup)
    elif user == 'client':
        bot.send_message(message.chat.id, text=messages.SEARCHING_IS_NOT_ALLOWED)
    else:
        start(message)


@bot.message_handler(regexp='Создать тикет')
def create_new_ticket(message: telebot.types.Message):
    """Создаем новый тикет"""
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id])
    user = db_client.who_is_it(message.from_user.id)
    if user == 'client':
        bot_message_id = bot.send_message(message.chat.id, text=messages.INPUT_TITLE).id
        bot.register_next_step_handler(message,
                                       get_title,
                                       bot_message_id=bot_message_id)
    elif user == 'freelancer':
        bot.send_message(message.chat.id, text=messages.CREATING_IS_NOT_ALLOWED)
    else:
        start(message)


def get_title(message: telebot.types.Message, bot_message_id: int):
    """Получаем от клиента название тикета"""
    ticket = dict(
        title=message.text
    )
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id, bot_message_id])
    bot_message_id = bot.send_message(message.chat.id, text=messages.INPUT_TICKET_TEXT).id
    bot.register_next_step_handler(message,
                                   get_text,
                                   ticket=ticket,
                                   bot_message_id=bot_message_id)


def get_text(message: telebot.types.Message, ticket: dict, bot_message_id: int):
    """Получаем от клиента текст тикета"""
    ticket['text'] = message.text
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id, bot_message_id])
    bot_message_id = bot.send_message(message.chat.id, text=messages.INPUT_TICKET_RATE).id
    bot.register_next_step_handler(message,
                                   get_rate,
                                   ticket=ticket,
                                   bot_message_id=bot_message_id)


def get_rate(message: telebot.types.Message, ticket: dict, bot_message_id: int):
    """Получаем от клиента стоимость работ по тикету"""
    try:
        ticket['rate'] = int(message.text)
    except ValueError:
        delete_messages(chat_id=message.chat.id, mes_ids=[message.id, bot_message_id])
        bot_message_id = bot.send_message(message.chat.id, text=messages.RATE_ERROR).id
        bot.register_next_step_handler(message,
                                       get_rate,
                                       ticket=ticket,
                                       bot_message_id=bot_message_id)
        return

    delete_messages(chat_id=message.chat.id, mes_ids=[message.id, bot_message_id])
    bot.send_message(message.chat.id,
                     text=messages.TICKET_CREATED.format(**ticket),
                     parse_mode='HTML')
    db_client.create_ticket(telegram_id=message.chat.id, **ticket)
    show_main_menu(message)


@bot.message_handler(regexp='Мои тикеты')
def show_client_tickets(message: telebot.types.Message):
    """Выводим список тикетов клиента"""
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id])
    bot.send_message(message.chat.id,
                     messages.MY_TICKETS,
                     reply_markup=markups.get_tickets_list())


@bot.message_handler(regexp='Заказы в работе')
def show_freelancer_orders(message: telebot.types.Message):
    """Выводим список заказов фрилансера"""
    delete_messages(chat_id=message.chat.id, mes_ids=[message.id])
    bot.send_message(message.chat.id,
                     messages.MY_ORDERS,
                     reply_markup=markups.get_orders_list())


@bot.callback_query_handler(func=lambda call: call.data.startswith('ticket_'))
def show_ticket_info(call: telebot.types.CallbackQuery):
    """Отображаем информацию по тикету"""
    # ticket = db_client.show_ticket(int(call.data.strip('ticket_')))
    ticket = {
        'title': 'Построить дом',
        'created_at': '17.02.23',
        'text': 'Из кирпича',
        'rate': 5000,
        'status': 'В работе',
        'freelancer': 'Вася',
        'estimate_time': '17.02.24',
        'completed_at': 'н/а'
    }
    ticket_markup = None

    user_role = db_client.who_is_it(call.message.chat.id)
    if user_role == 'client' and ticket['status'] != messages.TICKET_INFO['waiting']:
        ticket_markup = markups.make_inline_markups_from_dict({'Отправить сообщение': 'send_mes_to_freelancer',
                                                               'Читать переписку': 'show_chat'})
    if user_role == 'freelancer':
        if ticket['status'] == messages.TICKET_INFO['waiting']:
            ticket_markup = markups.make_inline_markups_from_dict({'Взять в работу': 'take_ticket'})
        elif ticket['status'] != messages.TICKET_INFO['waiting']:
            ticket_markup = markups.make_inline_markups_from_dict({'Отправить сообщение': 'send_mes_to_client',
                                                                   'Читать переписку': 'show_chat'})

    bot.answer_callback_query(call.id, text='Информация по тикету')
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
        'rate': 5000,
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
