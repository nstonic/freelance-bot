from peewee import IntegrityError
from peewee import fn, JOIN

from models import Client, Freelancer, Ticket, Order


def who_is_it(telegram_id: int) -> str:
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
        Freelancer.create(telegram_id=telegram_id, access=True)
        return True
    except IntegrityError:
        return False


def create_ticket(telegram_id: int, title: str, text: str, rate: float) -> bool:
    """Создает в базе тикет и возвращает True."""
    client = Client.get(telegram_id=telegram_id)
    Ticket.create(client=client, title=title, text=text, rate=rate)
    return True


def find_tickets() -> list:
    """Возвращает список из 5 случайных открытых тикетов (это для фрилансера)."""
    free_random_tickets = Ticket.select() \
        .join(Order, JOIN.LEFT_OUTER) \
        .where((Order.status==None) | (Order.status=='cancelled')) \
        .order_by(fn.Random()) \
        .limit(5)
    return list(free_random_tickets)


def show_order(order_id: int) -> Order:
    """Возвращает информацию по конкретному заказу."""
    pass


def show_tickets(telegram_id: int) -> list:
    """Возвращает список всех незакрытых тикетов заказчика."""
    pass


def show_ticket(ticket_id: int) -> Ticket:
    """Возвращает информацию по конкретному тикету."""
    pass
