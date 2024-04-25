from django.urls import include, path
# from rest_framework.routers import DefaultRouter

from api.views import LoginView

app_name = 'api'

# router = DefaultRouter()

# router.register('users', UserViewSet, basename='users')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('verify/<pk>', VerifyView.as_view(), name="verify"),
    # path('profile/', ProfileView.as_view(), name='profile')
]
