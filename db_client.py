import datetime

from peewee import IntegrityError
from peewee import fn

from models import Client, Freelancer, Ticket, Order, Message


def who_is_it(telegram_id: int) -> str:
    """Определяет в какой таблице зарегистрирован пользователь.
    Возвращает соответственно 'client' или 'freelancer'. Если пользователь не найден, возвращает None"""
    if Client.get_or_none(telegram_id=telegram_id):
        return 'client'
    elif Freelancer.get_or_none(telegram_id=telegram_id):
        return 'freelancer'


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
        .where(Ticket.status == 'waiting') \
        .order_by(fn.Random()) \
        .limit(5)
    return list(free_random_tickets)


def delete_ticket(ticket_id) -> bool:
    """Удаляет тикет"""
    try:
        Ticket.get(id=ticket_id).delete_instance()
        return True
    except Ticket.DoesNotExist:
        return False


def show_order(order_id: int) -> dict:
    """Возвращает информацию по конкретному заказу."""
    order = Order.get(id=order_id)
    serialized_order = {
        'ticket_id': order.ticket.id,
        'client': order.ticket.client.telegram_id,
        'title': order.ticket.title,
        'started_at': order.started_at,
        'text': order.ticket.text,
        'status': order.status,
        'freelancer': order.freelancer.telegram_id,
        'estimate_time': order.estimate_time,
        'completed_at': order.completed_at
    }
    return serialized_order


def show_my_orders(telegram_id: int) -> list:
    """Возвращает все не закрытые заказы фрилансера"""
    freelancer = Freelancer.get(telegram_id=telegram_id)
    return list(freelancer.orders.where(Order.status == 'in_progress'))


def start_work(ticket_id: int, telegram_id: int, estimate_time: datetime.date) -> int:
    """Фрилансер берет в работу тикет"""
    freelancer = Freelancer.get(telegram_id=telegram_id)
    ticket = Ticket.get(id=ticket_id)
    order = Order.create(
        ticket=ticket,
        freelancer=freelancer,
        estimate_time=estimate_time
    )
    ticket.status = 'in_progress'
    ticket.save()
    return order.id


def show_tickets(telegram_id: int) -> list:
    """Возвращает список всех незакрытых тикетов заказчика."""
    uncomplited_tickets = Client.get(telegram_id=telegram_id) \
        .tickets \
        .where(Ticket.status != 'finished')
    return list(uncomplited_tickets)


def show_ticket(ticket_id: int) -> dict:
    """Возвращает информацию по конкретному тикету."""
    ticket = Ticket.get(id=ticket_id)
    serialized_ticket = {
        'client': ticket.client.telegram_id,
        'order_id': get_order_id(ticket),
        'title': ticket.title,
        'created_at': ticket.created_at,
        'text': ticket.text,
        'status': ticket.status,
        'freelancer': get_ticket_freelancer(ticket),
        'estimate_time': get_ticket_estimate_time(ticket),
        'completed_at': get_ticket_complited_at(ticket)
    }
    return serialized_ticket


def get_ticket_freelancer(ticket):
    if ticket.orders:
        return ticket.orders.order_by(Order.started_at.desc()).first().freelancer.telegram_id


def get_ticket_estimate_time(ticket):
    if ticket.orders:
        return ticket.orders.order_by(Order.started_at.desc()).first().estimate_time


def get_ticket_complited_at(ticket):
    if ticket.orders:
        return ticket.orders.order_by(Order.started_at.desc()).first().completed_at


def get_order_id(ticket):
    if ticket.orders:
        return ticket.orders.order_by(Order.started_at.desc()).first().id


def close_order(order_id) -> bool:
    """Исполнитель закрывает заказ (ставим статус finished)"""
    order = Order.get(id=order_id)
    order.status = 'finished'
    order.completed_at = datetime.datetime.now()
    order.save()
    ticket = order.ticket
    ticket.status = 'finished'
    ticket.save()
    return True


def cancel_order(order_id) -> bool:
    """Исполнитель отказывается от заказа (ставим статус cancelled)"""
    order = Order.get(id=order_id)
    order.status = 'cancelled'
    order.completed_at = datetime.datetime.now()
    order.save()
    ticket = order.ticket
    ticket.status = 'waiting'
    ticket.save()
    return True

#  ********************  Чат  ********************  #


def show_chat(order_id) -> list:
    """Возвращает переписку по данному ордеру."""
    order = Order.get(id=order_id)
    messages = []
    for message in order.messages.order_by(Message.sending_at):
        serialized_message = {
            'user_role': message.user_role,
            'text': message.text,
            'sending_at': message.sending_at
        }
        messages.append(serialized_message)
    return messages


def create_chat_msg(order_id: int, telegram_id: int, message_text: str) -> bool:
    """Записываем сообщение в чат"""
    order = Order.get(id=order_id)
    user_role = who_is_it(telegram_id)
    Message.create(order=order, user_role=user_role, text=message_text)
    return True
