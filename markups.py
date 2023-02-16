from telebot import types


def register() -> types.InlineKeyboardMarkup:
    """Кнопка с предложением зарегистрироваться"""
    register_markup = types.InlineKeyboardMarkup(row_width=1)
    register_markup.add(types.InlineKeyboardButton(text="Зарегистрироваться", callback_data="register"))
    return register_markup


def choose_roll() -> types.InlineKeyboardMarkup:
    """Кнопки регистрации нового пользователя"""
    choose_roll_markup = types.InlineKeyboardMarkup(row_width=1)
    btn_client = types.InlineKeyboardButton(text="Заказчик", callback_data="roll_client")
    btn_freelancer = types.InlineKeyboardButton(text="Исполнитель", callback_data="roll_freelancer")
    choose_roll_markup.add(btn_client, btn_freelancer)
    return choose_roll_markup


def get_orders_list() -> types.InlineKeyboardMarkup:
    """Создает кнопки текущих заказов фрилансера"""
    my_orders_markup = types.InlineKeyboardMarkup(row_width=2)
    for btn in range(5):  # Пока просто 5 кнопок
        my_orders_markup.add(types.InlineKeyboardButton(text=btn, callback_data=f"order_{btn}"))
    return my_orders_markup


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
