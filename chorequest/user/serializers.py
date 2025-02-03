"""Module contains serializers for user registration, login, and password reset."""

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        """Meta class for RegisterSerializer."""

        model = User
        fields: ClassVar[list[str]] = ["id", "username", "email", "password", "confirm_password", "date_of_birth"]

    def validate(self, data: dict) -> dict:
        """Validate the user registration data."""
        # Sicherstellen, dass die Passwörter übereinstimmen
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"detail": "Passwords do not match."})

        return data

    def create(self, validated_data: dict) -> AuthUser:
        """Create a new user with the validated data."""
        # Entfernen der confirm_password, da wir es nicht speichern müssen
        validated_data.pop("confirm_password")

        # Benutzer erstellen
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data: dict) -> dict:
        """Validate the user login data."""
        from django.contrib.auth import authenticate
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            error_message = "Invalid username or password"
            raise serializers.ValidationError(error_message)
        tokens = RefreshToken.for_user(user)
        return {
            "refresh": str(tokens),
            "access": str(tokens.access_token),
            "user_id": user.id,
            "username": user.username,
        }

class PasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting a password reset email."""

    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        """Validate that the email exists in the database."""
        if not User.objects.filter(email=value).exists():
            error_message = "No user is associated with this email address."
            raise serializers.ValidationError(error_message)
        return value

    def save(self) -> None:
        """Send a password reset email to the user."""
        user = User.objects.get(email=self.validated_data["email"])
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        full_link = f"http://127.0.0.1:8000{reset_link}"

        # Sende die E-Mail
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {full_link}",
            "noreply@chorequest.com",
            [user.email],
        )
