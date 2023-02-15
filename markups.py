from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#  Регистрация нового пользователя
choose_roll = InlineKeyboardMarkup(row_width=1)
btn_client = InlineKeyboardButton(text="Заказчик", callback_data="roll_client")
btn_freelancer = InlineKeyboardButton(text="Исполнитель", callback_data="roll_freelancer")
choose_roll.add(btn_client)
choose_roll.add(btn_freelancer)

#  Список текущих заказов
my_orders = InlineKeyboardMarkup(row_width=2)
for btn in range(5):
    btn_client = InlineKeyboardButton(text=btn, callback_data=f"order_{btn}")
    my_orders.add(btn_client)
