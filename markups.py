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

