from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

choose_roll = InlineKeyboardMarkup(row_width=2)
btn_quiz = InlineKeyboardButton(text="Заказчик", callback_data="roll_client")
btn_info = InlineKeyboardButton(text="Исполнитель", callback_data="roll_doer")
choose_roll.add(btn_quiz)
choose_roll.add(btn_info)