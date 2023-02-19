from telebot import types


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


def get_order_buttons(order_id: int) -> types.InlineKeyboardMarkup:
    order_inline_markup = types.InlineKeyboardMarkup(row_width=2)
    close_btn = types.InlineKeyboardButton(text='Завершить', callback_data=f'close_order_{order_id}')
    cancel_btn = types.InlineKeyboardButton(text='Отказаться', callback_data=f'cancel_order_{order_id}')
    order_inline_markup.add(close_btn, cancel_btn)
    order_inline_markup.add(types.InlineKeyboardButton(text='Чат', callback_data=f'show_chat_order_{order_id}'))
    return order_inline_markup


def get_notice_buttons(show_answer: bool, order_id: int = None, ticket_id: int = None) -> types.InlineKeyboardMarkup:
    notice_buttons = types.InlineKeyboardMarkup(row_width=2)
    open_btn = None
    if ticket_id:
        open_btn = types.InlineKeyboardButton(text='Открыть тикет', callback_data=f'ticket_{ticket_id}')
    if order_id:
        open_btn = types.InlineKeyboardButton(text='Открыть заказ', callback_data=f'order_{order_id}')
    if show_answer:
        answer_btn = types.InlineKeyboardButton(text='Ответить', callback_data=f'answer_order_{order_id}')
    else:
        answer_btn = None
    notice_buttons.add(answer_btn, open_btn)
    return notice_buttons


def get_back_main_menu() -> types.ReplyKeyboardMarkup:
    return make_menu_from_list(['Назад', 'Основное меню'])
