import time


def send_sms_with_token(phone: str, token: str):
    """Имитация отправки сообщения на номер телефона (в фоновом режиме)."""
    time.sleep(2)
    print((f'Отправка смс на номер телефона {phone}.'
           f'Для входа введите: {token}'))
    return True
