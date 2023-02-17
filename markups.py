from telebot import types

import models


def make_inline_markups_from_dict(buttons: dict) -> types.InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup из словаря 'текст_кнопки':'callback_data' """
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(*[types.InlineKeyboardButton(text=button, callback_data=callback)
                 for button, callback in buttons.items()])
    return markup


def make_menu_from_list(buttons: list) -> types.ReplyKeyboardMarkup:
    """Создаёт меню из списка кнопок"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(button) for button in buttons])
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
