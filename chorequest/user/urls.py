"""URL configuration for the user app."""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, PasswordResetView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password/forgot/", PasswordResetView.as_view(), name="password_reset_api"),
]
