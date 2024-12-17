from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "date_of_birth"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
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

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def save(self):
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