from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


from users.models import User
from api.serializers import LoginSerializer


class LoginView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
