from peewee import IntegrityError

from models import Client, Freelancer


def who_is_it(telegram_id: int) -> str | None:
    """Определяет в какой таблице зарегистрирован пользователь.
    Возвращает соответственно 'client' или 'freelancer'. Если пользователь не найден, возвращает None"""
    if Client.get_or_none(telegram_id=telegram_id):
        return 'client'
    elif Freelancer.get_or_none(telegram_id=telegram_id):
        return 'freelancer'
    return None


def register_client(telegram_id: int) -> bool:
    """Регистрирует пользователя в таблице Client. Возвращает True после успешной регистрации"""
    try:
        Client.create(telegram_id=telegram_id)
        return True
    except IntegrityError:
        return False


def register_freelancer(telegram_id: int) -> bool:
    """Регистрирует пользователя в таблице Freelancer. Возвращает True после успешной регистрации"""
    try:
        Freelancer.create(telegram_id=telegram_id)
        return True
    except IntegrityError:
        return False


def find_orders(chat_id: int) -> list:
    """Возвращает список из 5 случайных открытых тикетов (это для фрилансера"""
    pass


def show_order(order_id: int) -> dict:
    """Возвращает информацию по конкретному заказу"""
    pass


def show_tickets(chat_id: int) -> list:
    """Возвращает список всех незакрытых тикетов заказчика"""
    pass


def show_ticket(ticket_id: int) -> dict:
    """Возвращает информацию по конкретному тикету"""
    pass
