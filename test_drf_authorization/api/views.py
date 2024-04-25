from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import LoginSerializer
from api.tasks import send_sms_with_token
from users.models import CallbackToken, User


class LoginView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, user_exist = User.objects.get_or_create(
            phone=serializer.validated_data['phone']
        )
        if not user_exist:
            serializer.save()
        callback_token = CallbackToken.objects.filter(user=user).first()
        send_sms_with_token(user, callback_token)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyViewView(CreateAPIView):
    pass
