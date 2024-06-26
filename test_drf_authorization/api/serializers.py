from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

from api.validators import age_token_validator
from users.models import CallbackToken, User
from users.utils import create_key

VERIFY_ERROR_MASSAGE = {
    'required_data': 'Должны быть переданны  <token> и <phone>!',
    'invalid_user': 'Указан неверный пользователь!',
    'invalid_token': 'Указан неверный токен!',
    'invalid_parameters': 'Указаны неверные параметры'
}

PROFILE_ERROR_MASSAGE = {
    'reactivation': 'Вы уже активировали <invite_code>',
    'invalid_invite_code': 'Указан несуществующий <invite_code>!',

}


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    phone = PhoneNumberField(required=True)

    class Meta:
        model = User
        read_only_fields = ('id', )
        fields = ('id', 'phone',)

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        token, create = CallbackToken.objects.get_or_create(user=user)
        if not create:
            token.key = create_key()
            token.is_active = True
            token.created_at = timezone.now()
        token.save()
        return user


class TokenSerializer (serializers.Serializer):
    """Сериализатор токена."""
    token = serializers.CharField(source='key')
    key = serializers.CharField(write_only=True)


class VerifySerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    token = serializers.CharField(min_length=settings.KEY_LENGTH,
                                  max_length=settings.KEY_LENGTH,
                                  validators=[age_token_validator])

    def validate(self, data):
        token = data.get('token', None)
        phone = data.get('phone', None)
        if token is None or phone is None:
            raise serializers.ValidationError(
                VERIFY_ERROR_MASSAGE['required_data']
            )
        try:
            user = User.objects.get(phone=phone)
            CallbackToken.objects.get(user=user,
                                      key=token,
                                      is_active=True)
            data['user'] = user
            user.is_verified = True
            user.save()

        except User.DoesNotExist:
            raise serializers.ValidationError(
                VERIFY_ERROR_MASSAGE['invalid_user']
            )
        except CallbackToken.DoesNotExist:
            raise serializers.ValidationError(
                VERIFY_ERROR_MASSAGE['invalid_token']
            )
        except ValidationError:
            raise serializers.ValidationError(
                VERIFY_ERROR_MASSAGE['invalid_parameters']
            )
        else:
            return data


class ForeignInviteSerializer (serializers.ModelSerializer):
    """Сериализатор пользователей с инвайткодом пользователя."""

    class Meta:
        model = User
        read_only_fields = ('phone', )
        fields = ('phone',)


class ProfileSerializer (serializers.ModelSerializer):
    """Сериализатор токена. """
    foreign_invite_code = serializers.CharField(write_only=True)
    activated_your_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        read_only = ('id', 'phone', 'invite_code', 'activated_your_code')
        fields = ('id', 'phone',
                  'invite_code',
                  'foreign_invite_code',
                  'activated_your_code')

    def get_activated_your_code(self, obj: User) -> list:
        queryset = User.objects.filter(foreign_invite_code=obj)
        return [ForeignInviteSerializer(user).data for user in queryset]

    def validate(self, data):
        new_foreign_invite_code = self.initial_data.get('foreign_invite_code')
        foreign_invite_code = self.instance.foreign_invite_code

        if new_foreign_invite_code:
            if foreign_invite_code:
                raise serializers.ValidationError(
                    PROFILE_ERROR_MASSAGE['reactivation']
                )
            try:
                foreign_user = User.objects.get(
                    invite_code=new_foreign_invite_code
                )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    PROFILE_ERROR_MASSAGE['invalid_invite_code']
                )
            except ValidationError:
                raise serializers.ValidationError(
                    VERIFY_ERROR_MASSAGE['invalid_parameters']
                )
            else:
                self.instance.foreign_invite_code = foreign_user
                self.instance.save()
        return data
