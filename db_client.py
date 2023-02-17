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


def register_user(telegram_id: int, role: str) -> bool:
    """Регистрирует пользователя в таблице Client или Freelancer в зависимости от роли. Возвращает True после успешной регистрации"""
    try:
        if role == 'client':
            Client.create(telegram_id=telegram_id)
        elif role == 'freelancer':
            Freelancer.create(telegram_id=telegram_id, access=True)
        return True
    except IntegrityError:
        return False


def create_ticket(telegram_id: int, title: str, text: str, rate=5000.0) -> bool:
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
    uncomplited_tickets = Client.get(telegram_id=telegram_id) \
        .tickets \
        .select(Ticket, Order) \
        .join(Order, JOIN.LEFT_OUTER) \
        .where((Order.status==None) | (Order.status!='complete'))
    return list(uncomplited_tickets)


def show_ticket(ticket_id: int) -> dict:
    """Возвращает информацию по конкретному тикету."""
    ticket = Ticket.get(id=ticket_id)
    pass
