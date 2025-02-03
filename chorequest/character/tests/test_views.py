"""Module containing tests for the CharacterViewSet."""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import UserAccount

from character.models import Character


class CharacterViewSetTest(APITestCase):
    """Teste den CharacterViewSet."""

    def setUp(self) -> None:
        """Setze die Testdaten."""
        UserAccount.objects.all().delete()
        Character.objects.all().delete()

        login_data = {
            "username": "testuser1",
            "password": "password123",
        }

        self.user1 = get_user_model().objects.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="password123",  # noqa: S106
            date_of_birth="2000-01-01",
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="password123",  # noqa: S106
            date_of_birth="2000-01-01",
        )

        # Erstelle einen Charakter für user1
        self.character1 = Character.objects.create(
            user=self.user1,
            name="Hero123",
            level=1,
            experience_points=0,
        )

        # Erstelle einen Charakter für user2
        self.character2 = Character.objects.create(
            user=self.user2,
            name="Warrior456",
            level=1,
            experience_points=0,
        )

        login_response = self.client.post("/api/user/login/", login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)  # Stelle sicher, dass das access_token da ist

        self.access_token = login_response.data["access"]

    def test_login_success(self) -> None:
        """Teste, ob ein Benutzer mit gültigen Anmeldedaten eingeloggt werden kann."""
        login_response = self.client.login(username="testuser1", password="password123")  # noqa: S106

        # Überprüfe, ob das Login erfolgreich war (True zurückgeben bedeutet erfolgreicher Login)
        self.assertTrue(login_response)

        # Überprüfe, ob der eingeloggte Benutzer die richtige ID hat
        response = self.client.get("/api/characters/", HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)  # Ein erfolgreicher Authenticated Request

    def test_login_fail(self) -> None:
        """Teste, ob ein Benutzer mit falschen Anmeldedaten nicht eingeloggt werden kann."""
        login_response = self.client.login(username="testuser1", password="wrongpassword")  # noqa: S106

        # Überprüfe, dass das Login nicht erfolgreich war
        self.assertFalse(login_response)

    def test_create_character(self) -> None:
        """Teste, ob ein authentifizierter Benutzer einen neuen Charakter erstellen kann."""
        data = {
            "name": "Mage789",
            "level": 1,
            "experience_points": 0,
        }

        response = self.client.post(
            "/api/characters/",
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 3)  # Es sollte jetzt 3 Charaktere geben

        # Überprüfe, ob der Charakter dem richtigen Benutzer zugewiesen wurde
        new_character = Character.objects.latest("id")
        self.assertEqual(new_character.user, self.user1)

    def test_create_character_unauthorized(self) -> None:
        """Teste, ob ein nicht authentifizierter Benutzer keinen Charakter erstellen kann."""
        self.client.logout()  # Logout user1

        data = {
            "name": "Mage789",
            "level": 1,
            "experience_points": 0,
        }

        response = self.client.post("/api/characters/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Erwartete Antwort: Unauthorized

    def test_list_own_characters(self) -> None:
        """Teste, ob ein Benutzer nur seine eigenen Charaktere sehen kann."""
        response = self.client.get("/api/characters/", format="json", HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.character1.id)

    def test_get_own_characters(self) -> None:
        """Teste, ob ein Benutzer seine eigenen Charaktere sehen kann."""
        character_id = self.character1.id
        response = self.client.get(
            f"/api/characters/{character_id}/",
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data

        self.assertEqual(response_data["id"], character_id)
        self.assertEqual(response_data["name"], "Hero123")

    def test_get_other_users_characters(self) -> None:
        """Teste, ob ein Benutzer nicht die Charaktere eines anderen Benutzers sehen kann."""
        character_id = self.character2.id
        response = self.client.get(
            f"/api/characters/{character_id}/",
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_character(self) -> None:
        """Teste, ob ein Benutzer seinen eigenen Charakter löschen kann."""
        response = self.client.delete(
            f"/api/characters/{self.character1.id}/",
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Character.objects.count(), 1)

    def test_delete_other_users_character(self) -> None:
        """Teste, ob ein Benutzer nicht den Charakter eines anderen Benutzers löschen kann."""
        response = self.client.delete(
            f"/api/characters/{self.character2.id}/",
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
