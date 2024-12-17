from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import UserAccount




class UserRegistrationTestCase(APITestCase):
    """Tests for user registration endpoint."""

    def setUp(self):
        """Clean the database before each test."""
        UserAccount.objects.all().delete()

    def test_registration_successful(self):
        """Test registering a new user successfully."""
        url = reverse("register")
        data = {
            "username": "automatedtestuser",
            "email": "mytestemail@example.com",
            "password": "securepassword",
            "date_of_birth": "2000-01-01",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserAccount.objects.count(), 1)
        self.assertEqual(UserAccount.objects.get().username, "automatedtestuser")

    def test_registration_missing_fields(self):
        """Test registration fails if fields are missing."""
        url = reverse("register")
        data = {"username": "testuser"}  # Fehlende Felder
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginTestCase(APITestCase):
    """Tests for user login endpoint."""

    def setUp(self):
        UserAccount.objects.all().delete()
        self.user = UserAccount.objects.create_user(
            username="testuser", email="test@example.com", password="securepassword"
        )

    def test_login_successful(self):
        """Test login with valid credentials."""
        url = reverse("login")
        data = {"username": "testuser", "password": "securepassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        url = reverse("login")
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PasswordResetTestCase(APITestCase):
    """Tests for the password reset endpoint."""

    def setUp(self):
        """Set up a test user."""
        UserAccount.objects.all().delete()
        self.user = UserAccount.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword"
        )
        self.password_reset_url = reverse("password_reset_api")

    def test_password_reset_email_sent(self):
        """Test that a password reset email is sent for a valid email."""
        data = {"email": "test@example.com"}
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset email sent.")

    def test_password_reset_invalid_email(self):
        """Test that an error is returned for a non-existing email."""
        data = {"email": "nonexistent@example.com"}
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No user is associated with this email address.", str(response.data))