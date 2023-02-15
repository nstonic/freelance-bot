def who_is_it(telegram_id: str) -> str | None:
    """Определяет в какой таблице зарегистрирован пользователь.
    Возвращет соответственно 'client' или 'freelancer'. Если пользователь не найден, возвращает None"""


def register_client(telegram_id: str) -> bool:
    """Регистрирует пользователя в таблице Client. Возвращает True после успешной регистрации"""


def register_freelancer(telegram_id: str) -> bool:
    """Регистрирует пользователя в таблице Freelancer. Возвращает True после успешной регистрации"""
