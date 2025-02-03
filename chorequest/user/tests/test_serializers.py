"""Tests for user registration serializers."""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_password_mismatch(client: Client) -> None:
    """Test registration fails when passwords do not match."""
    url = reverse("register")  # Name der URL-Route für die Registrierung
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "confirm_password": "password321",  # Unterschiedliches Passwort
        "date_of_birth": "2000-01-01",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": ["Passwords do not match."]}

@pytest.mark.django_db
def test_email_already_exists(client: Client) -> None:
    """Test registration fails when the email already exists."""
    # Erstelle einen Benutzer mit derselben E-Mail
    User.objects.create_user(username="existinguser", email="existing@example.com", password="password123")  # noqa: S106

    url = reverse("register")
    payload = {
        "username": "newuser",
        "email": "existing@example.com",  # Bereits verwendete E-Mail
        "password": "password123",
        "confirm_password": "password123",
        "date_of_birth": "2000-01-01",
    }

    response = client.post(url, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"email": ["user with this email already exists."]}
