from telebot.types import (InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton)


def make_inline_markups_from_dict(btns: dict, row_width: int = 2) -> InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup из словаря 'текст_кнопки':'callback_data' """
    markup = InlineKeyboardMarkup(row_width=row_width)
    buttons = [InlineKeyboardButton(text=button, callback_data=callback)
               for button, callback in btns.items()]
    markup.add(*buttons)
    return markup


def make_menu_from_list(buttons_title: list, row_width: int = 2) -> ReplyKeyboardMarkup:
    """Создаёт меню из списка кнопок"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(button)
               for button in buttons_title]
    markup.add(*buttons, row_width=row_width)
    return markup


def get_order_buttons(order_id: int) -> InlineKeyboardMarkup:
    order_inline_markup = InlineKeyboardMarkup(row_width=2)
    close_btn = InlineKeyboardButton(text='Завершить', callback_data=f'close_order_{order_id}')
    cancel_btn = InlineKeyboardButton(text='Отказаться', callback_data=f'cancel_order_{order_id}')
    order_inline_markup.add(close_btn, cancel_btn)
    order_inline_markup.add(InlineKeyboardButton(text='Чат', callback_data=f'show_chat_order_{order_id}'))
    return order_inline_markup


def get_notice_buttons(user_role: str, order_id: int,
                       ticket_id: int) -> InlineKeyboardMarkup:
    notice_buttons = InlineKeyboardMarkup(row_width=2)
    if user_role == 'client':
        notice_buttons.add(InlineKeyboardButton(text='Открыть тикет', callback_data=f'ticket_{ticket_id}'))
    if user_role == 'freelancer':
        notice_buttons.add(InlineKeyboardButton(text='Открыть заказ', callback_data=f'order_{order_id}'))
    return notice_buttons


def get_back_main_menu() -> ReplyKeyboardMarkup:
    return make_menu_from_list(['Назад', 'Основное меню'])
