"""Module contains views for user registration, login, and password reset."""

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, PasswordResetSerializer, RegisterSerializer

User = get_user_model()

# Registration View
class RegisterView(generics.CreateAPIView):
    """API View for user registration."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request: Request) -> Response:
        """Handle POST request for user registration."""
        # Erstelle den Serializer mit den gesendeten Daten
        serializer = self.get_serializer(data=request.data)

        # Versuche, den Benutzer zu erstellen
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"detail": "Registration successful!"}, status=status.HTTP_201_CREATED)

        # Fehlerbehandlung: Wenn die Validierung fehlschlägt, gib benutzerdefinierte Fehlermeldungen zurück
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    """API View for user login."""

    def post(self, request: Request) -> Response:
        """Handle POST request for password reset."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class PasswordResetView(GenericAPIView):
    """API View for requesting a password reset email."""

    serializer_class = PasswordResetSerializer

    def post(self, request: Request) -> Response:
        """Handle POST request for password reset."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
