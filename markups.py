from telebot import types

import models


def make_inline_markups_from_dict(btns: dict, row_width: int = 2) -> types.InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup из словаря 'текст_кнопки':'callback_data' """
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    buttons = [types.InlineKeyboardButton(text=button, callback_data=callback)
               for button, callback in btns.items()]
    markup.add(*buttons)
    return markup


def make_menu_from_list(buttons_title: list, row_width: int = 2) -> types.ReplyKeyboardMarkup:
    """Создаёт меню из списка кнопок"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(button)
               for button in buttons_title]
    markup.add(*buttons, row_width=row_width)
    return markup


def get_back_main_menu() -> types.ReplyKeyboardMarkup:
    return make_menu_from_list(['Назад', 'Основное меню'])


def get_orders_list(orders: list[models.Order]) -> types.InlineKeyboardMarkup:
    """Создает кнопки текущих заказов фрилансера"""
    my_orders_markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(
        text=order.ticket.title,
        callback_data=f"order_{order.get_id()}"
    ) for order in orders]
    my_orders_markup.add(*buttons)
    return my_orders_markup


def get_tickets_list_inline(tickets: list[models.Ticket]) -> types.InlineKeyboardMarkup:
    """Создает кнопки для выбора тикета"""
    tickets_choose_markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(
        text=ticket.title,
        callback_data=f"ticket_{ticket.get_id()}"
    ) for ticket in tickets]
    tickets_choose_markup.add(*buttons)
    return tickets_choose_markup
