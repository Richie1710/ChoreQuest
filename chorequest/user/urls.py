from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password/forgot/", PasswordResetView.as_view(), name="password_reset_api"),
]