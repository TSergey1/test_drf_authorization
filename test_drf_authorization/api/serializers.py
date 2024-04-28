from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

from api.validators import age_token_validator
from users.models import CallbackToken, User

VERIFY_ERROR_MASSAGE = {
    'required_data': 'Должны быть переданны  <token> и <phone>!',
    'invalid_user': 'Указан неверный пользователь!',
    'invalid_token': 'Указан неверный токен!',
    'invalid_parameters': 'Указаны неверные параметры'

}


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    phone = PhoneNumberField(required=True)

    class Meta:
        model = User
        read_only_fields = ('id', )
        fields = ('id', 'phone',)


class TokenSerializer (serializers.Serializer):
    """Сериализатор токена."""
    token = serializers.CharField(source='key')
    key = serializers.CharField(write_only=True)


class VerifySerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=True)
    token = serializers.CharField(min_length=settings.KEY_LENGTH,
                                  max_length=settings.KEY_LENGTH,
                                  validators=[age_token_validator])

    def validate(self, data):
        token = data.get('token', None)
        phone = data.get('phone', None)
        if token is not None or phone is not None:
            raise serializers.ValidationError(
                VERIFY_ERROR_MASSAGE['required_data']
            )
        try:
            user = User.objects.get(phone=phone)
            CallbackToken.objects.get(user=user,
                                      key=token,
                                      is_active=True).first()
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
