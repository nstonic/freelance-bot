from telebot import types

import models


def make_inline_markups_from_dict(buttons: dict) -> types.InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup из словаря 'текст_кнопки':'callback_data' """
    markup = types.InlineKeyboardMarkup()
    for button, callback in buttons.items():
        markup.add(types.InlineKeyboardButton(text=button, callback_data=callback))
    return markup


def get_orders_list() -> types.InlineKeyboardMarkup:
    """Создает кнопки текущих заказов фрилансера"""
    my_orders_markup = types.InlineKeyboardMarkup(row_width=2)
    for btn in range(5):  # Пока просто 5 кнопок
        my_orders_markup.add(types.InlineKeyboardButton(text=btn, callback_data=f"order_{btn}"))
    return my_orders_markup


def get_tickets_choose_btns(tickets: list[models.Ticket]) -> types.InlineKeyboardMarkup:
    """Создает кнопки для выбора тикета"""
    tickets_choose_markup = types.InlineKeyboardMarkup(row_width=2)
    for ticket in tickets:
        tickets_choose_markup.add(types.InlineKeyboardButton(text=ticket.title,
                                                             callback_data=f"ticket_{ticket.get_id()}"))
    return tickets_choose_markup


def get_tickets_list() -> types.InlineKeyboardMarkup:
    """Создает кнопки текущих тикетов заказчика"""
    my_tickets_markup = types.InlineKeyboardMarkup(row_width=2)
    for btn in range(5):
        my_tickets_markup.add(types.InlineKeyboardButton(text=btn, callback_data=f"ticket_{btn}"))
    return my_tickets_markup


def get_client_menu() -> types.ReplyKeyboardMarkup:
    """Меню клиента"""
    client_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_new_ticket = types.KeyboardButton("Создать тикет")
    btn_my_tickets = types.KeyboardButton("Мои тикеты")
    client_menu_markup.add(btn_my_tickets, btn_new_ticket)
    return client_menu_markup


def get_freelancer_menu() -> types.ReplyKeyboardMarkup:
    """Меню фрилансера"""
    freelancer_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_find_order = types.KeyboardButton("Найти заказ")
    btn_my_orders = types.KeyboardButton("Заказы в работе")
    freelancer_menu_markup.add(btn_my_orders, btn_find_order)
    return freelancer_menu_markup
