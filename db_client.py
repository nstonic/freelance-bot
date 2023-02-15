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
