import phonenumbers
from rest_framework import serializers

from users.models import User

ERROR_PHONE = 'Некорректный номер телефона'


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер User."""

    class Meta:
        model = User
        fields = ('email', 'phone', 'password')

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_telephone(self, value):
        if value[0] != '+':
            value = f'+{value}'
        telephone = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(telephone):
            raise serializers.ValidationError(ERROR_PHONE)
        return value
