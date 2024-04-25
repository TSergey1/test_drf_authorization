import random
import string
from django.contrib.auth import hashers

LENGHTH_INVATE_CODE = 6
ALLOWED_CHARS_INVATE_CODE = string.ascii_letters + string.digits
LENGHTH_TOKEN = 4
ALLOWED_CHARS_TOKEN = string.digits


def create_code(length: int = LENGHTH_INVATE_CODE,
                allowed_chars: str = ALLOWED_CHARS_INVATE_CODE) -> str:
    """
    Возвращает сгенерированный код состоящий из {length} символов и чисел.
    """

    return ''.join(random.choice(allowed_chars) for _ in range(length))


def create_token(length: int = LENGHTH_TOKEN,
                 allowed_chars: str = ALLOWED_CHARS_TOKEN) -> str:
    """Возвращает сгенерированный токен состоящий из {length} чисел."""

    return hashers.make_password(
        ''.join(random.choice(allowed_chars) for _ in range(length))
    )
