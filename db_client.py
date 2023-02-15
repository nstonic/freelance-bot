def who_is_it(telegram_id: int) -> str | None:
    """Определяет в какой таблице зарегистрирован пользователь.
    Возвращает соответственно 'client' или 'freelancer'. Если пользователь не найден, возвращает None"""
    return None


def register_client(telegram_id: int) -> bool:
    """Регистрирует пользователя в таблице Client. Возвращает True после успешной регистрации"""
    return True


def register_freelancer(telegram_id: int) -> bool:
    """Регистрирует пользователя в таблице Freelancer. Возвращает True после успешной регистрации"""
    return True
