import time


def send_sms_with_token(token: str) -> bool:
    """Имитация отправки сообщения на номер телефона (в фоновом режиме)."""
    time.sleep(2)
    return f'Код для регистрации {token}'
