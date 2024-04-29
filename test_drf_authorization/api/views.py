from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from api.serializers import (LoginSerializer, ProfileSerializer,
                             TokenSerializer, VerifySerializer)
from api.tasks import send_sms_with_token
from api.utils import create_token
from users.models import CallbackToken, User


class LoginView(CreateAPIView):
    """Получение пороля при регистрации."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            phone=serializer.validated_data['phone']
        )
        callback_token = CallbackToken.objects.filter(user=user).first()
        send_sms_with_token(user, callback_token)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyView(APIView):
    """Верификация пользователя по ключу."""

    permission_classes = (AllowAny,)
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_token = create_token(serializer.validated_data['user'])
            if user_token:
                token_serializer = TokenSerializer(
                    data={'token': user_token.key, },
                    partial=True
                )
                if token_serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def putch(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(deprecated=True)
    def put(self):
        """Метод PUT запрещен"""
        raise NotImplementedError
