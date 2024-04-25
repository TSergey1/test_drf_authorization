import random
import string
from django.utils.crypto import get_random_string

LENGHTH_INVATE_CODE = 6
ALLOWED_CHARS = string.ascii_letters + string.digits

def create_code(length=LENGHTH_INVATE_CODE,
                       allowed_chars=ALLOWED_CHARS):
    """Возвращает сгенерированный код."""

    return ''.join(random.choice(allowed_chars) for i in range(length))


  def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        warnings.warn(
            "BaseUserManager.make_random_password() is deprecated.",
            category=RemovedInDjango51Warning,
            stacklevel=2,
        )
        return get_random_string(length, allowed_chars)