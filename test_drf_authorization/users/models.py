from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from users.utils import create_invate_code, create_key

HELP_TEXT_PHONE = 'Введите номер телефона в формате +7**********'


class UserManager(BaseUserManager):
    """Переопределяем мэнеджер пользователя."""
    use_in_migrations = True

    def create_user(self, phone, **extra_fields):
        """Создает и сохраняет пользователя с phone."""
        if not phone:
            raise ValueError('The given phone must be set')

        user, _ = User.objects.get_or_create(phone=phone,
                                             **extra_fields)
        if user.invite_code is None:
            user.invite_code = create_invate_code()
            user.save()
        token = CallbackToken.objects.create(user=user)
        token.save()
        return user

    def create_superuser(self, phone, **extra_fields):
        """Создает и сохраняет пользователя как суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(phone)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""
    password = None
    last_login = None
    phone = PhoneNumberField(unique=True, verbose_name='Номер телефона',
                             help_text=HELP_TEXT_PHONE)
    invite_code = models.CharField(
        max_length=6, default=create_invate_code(),
        verbose_name='Инвайт-код'
    )
    foreign_invite_code = models.ForeignKey('self',
                                            on_delete=models.SET_DEFAULT,
                                            null=True,
                                            default=None)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone


class CallbackToken(models.Model):
    """Модель данных токена подтверждения авторизации."""
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             related_name=None,
                             on_delete=models.CASCADE)
    key = models.CharField(default=create_key(),
                           max_length=settings.KEY_LENGTH)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Callback Token'
        ordering = ['id']

    def __str__(self):
        return str(self.key)
