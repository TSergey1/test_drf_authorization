from django.conf import settings
from django.utils import timezone

from users.models import CallbackToken


def age_token_validator(token) -> bool:
    """Проверка срока действия токена."""
    try:
        callback_token = CallbackToken.objects.filter(key=token,
                                                      is_active=True).first()
        token_life = timezone.now() - callback_token.created_at
        if token_life.total_seconds() < settings.TOKEN_EXPIRE_TIME:
            return True
        else:
            callback_token.is_active = False
            callback_token.save()
            return False

    except CallbackToken.DoesNotExist:
        return False
