from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import User


class LoginSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    phone = PhoneNumberField(required=True)

    class Meta:
        model = User
        read_only_fields = ('id', )
        fields = ('id', 'phone',)



# class LoginSerializer(serializers.ModelSerializer):
#     """Сериализатор регистрации."""
#     phone = PhoneNumberField(required=True)

#     class Meta:
#         model = User
#         read_only_fields = ('id', )
#         fields = ('id', )



        
