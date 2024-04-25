from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from users.utils import create_invite_code


class UserManager(BaseUserManager):
    """Переопределяем мэнеджер пользователя."""

    def create_user(self, phone, **kwargs):
        """Создает и сохраняет пользователя с phone."""
        if not phone:
            raise ValueError('The given phone must be set')

        user = User.objects.get_or_create(phone=phone)

        if user.referral_code is None:
            user.referral_code = create_code()
            user.save()

        token = CallbackToken.objects.create(user=user)
        token.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """Создает и сохраняет пользователя как суперпользователя."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""
    phone = PhoneNumberField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    invite_code = models.CharField(
        max_length=6, default=create_invite_code(),
        unique=True, verbose_name='Инвайт код'
    )
    else_invite_code = models.ForeignKey('self',
                                         on_delete=models.SET_DEFAULT,
                                         null=True,
                                         default=None)
    password = models.CharField(max_length=4,
                                verbose_name='Одноразовый пароль',
                                null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone

    # @property
    # def token(self):
    #     """
    #     Позволяет получить токен пользователя путем вызова user.token,
    #     вместо user._generate_jwt_token()
    #     """
    #     return self._generate_jwt_token()

    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя
    #     """
    #     dt = datetime.now() + timedelta(days=1)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #     return token.decode('utf-8')
