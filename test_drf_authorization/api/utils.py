from rest_framework.authtoken.models import Token


def create_token(user) -> Token:
    """Генерация токена для пользователя."""
    return Token.objects.get_or_create(user=user)[0]
