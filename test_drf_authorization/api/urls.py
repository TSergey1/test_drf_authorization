from django.urls import path

from api.views import LoginView, ProfileView, VerifyView

app_name = 'api'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', VerifyView.as_view(), name="verify"),
    path('profile/', ProfileView.as_view(), name='profile')
]
