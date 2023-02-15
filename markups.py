from telebot import types

#  Предложение зарегистрироваться
register = types.InlineKeyboardMarkup(row_width=1)
btn_register = types.InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")
register.add(btn_register)


#  Регистрация нового пользователя
choose_roll = types.InlineKeyboardMarkup(row_width=1)
btn_client = types.InlineKeyboardButton(text="Заказчик", callback_data="roll_client")
btn_freelancer = types.InlineKeyboardButton(text="Исполнитель", callback_data="roll_freelancer")
choose_roll.add(btn_client, btn_freelancer)

#  Список текущих заказов
my_orders = types.InlineKeyboardMarkup(row_width=2)
for btn in range(5):
    btn_client = types.InlineKeyboardButton(text=btn, callback_data=f"order_{btn}")
    my_orders.add(btn_client)

#  Меню клиента
client_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_new_order = types.KeyboardButton("Создать заказ")
btn_my_orders = types.KeyboardButton("Мои заказы")
client_menu.add(btn_my_orders, btn_new_order)

#  Меню фрилансера
freelancer_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_find_order = types.KeyboardButton("Найти заказ")
btn_my_orders = types.KeyboardButton("Заказы в работе")
freelancer_menu.add(btn_my_orders, btn_find_order)
