import string
from django.utils.crypto import get_random_string
# from django.contrib.auth import hashers

from django.conf import settings

ALLOWED_CHARS_INVATE_CODE = string.ascii_letters + string.digits
ALLOWED_CHARS_TOKEN = string.digits


def create_invate_code(length: int = settings.INVATE_CODE_LENGTH,
                       allowed_chars: str = ALLOWED_CHARS_INVATE_CODE) -> str:
    """
    Возвращает сгенерированный код состоящий из {length} символов и чисел.
    """
    return get_random_string(length, allowed_chars)


def create_key(length: int = settings.KEY_LENGTH,
               allowed_chars: str = ALLOWED_CHARS_TOKEN) -> str:
    """Возвращает сгенерированный токен состоящий из {length} чисел."""

    return get_random_string(length, allowed_chars)
