import time


def send_sms_with_token(phone: str, token: str) -> bool:
    """Имитация отправки сообщения на номер телефона (в фоновом режиме)."""
    time.sleep(2)
    try:
        print((f'Отправка смс на номер телефона {phone}.'
               f'Проверочный код: {token}'))
        return True
    except Exception:
        return False
