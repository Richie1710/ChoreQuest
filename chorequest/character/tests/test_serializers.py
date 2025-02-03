"""Module contains tests for the CharacterSerializer."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from character.serializers import CharacterSerializer


class CharacterSerializerTest(APITestCase):
    """Teste den CharacterSerializer."""

    def setUp(self) -> None:
        """Setze die Testdaten."""
        self.user = get_user_model().objects.create_user(
            username="testuserserializer",
            email="testuser@example.com",
            password="password123",  # noqa: S106
        )

    def test_character_serializer_valid(self) -> None:
        """Teste, ob der Serializer gültige Daten akzeptiert."""
        data = {
            "name": "SerializerHero123",
            "level": 1,
            "experience_points": 0,
        }

        serializer = CharacterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        character = serializer.save(user=self.user)
        self.assertEqual(character.name, "SerializerHero123")
        self.assertEqual(character.level, 1)
        self.assertEqual(character.experience_points, 0)
        self.assertEqual(character.user, self.user)

    def test_character_serializer_missing_name(self) -> None:
        """Teste, ob der Serializer fehlende Daten ablehnt."""
        data = {
            "level": 1,
            "experience_points": 0,
        }

        serializer = CharacterSerializer(data=data)
        self.assertFalse(serializer.is_valid())  # Überprüfe, ob der Serializer invalid ist
        self.assertIn("name", serializer.errors)  # Überprüfe, ob 'name' in den Fehlern ist

    def test_character_serializer_user_not_required(self) -> None:
        """Teste, ob der Benutzer nicht erforderlich ist."""
        data = {
            "name": "Warrior456",
            "level": 1,
            "experience_points": 0,
        }

        serializer = CharacterSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Der Serializer sollte gültig sein, auch ohne den Benutzer
        character = serializer.save(user=self.user)
        self.assertEqual(character.user, self.user)

    def test_character_serializer_negative_level(self) -> None:
        """Teste, ob der Serializer ungültige Daten ablehnt (z.B. nicht positive Level)."""
        data = {
            "name": "SerializerHero123",
            "level": -1,  # Ungültiger Wert für Level
            "experience_points": 0,
        }

        serializer = CharacterSerializer(data=data)
        self.assertFalse(serializer.is_valid())  # Der Serializer sollte invalid sein
        self.assertIn("level", serializer.errors)  # Überprüfe, ob 'level' in den Fehlern ist

    def test_character_serializer_negative_xp(self) -> None:
        """Teste, ob der Serializer ungültige Daten ablehnt (z.B. nicht positive XP)."""
        data = {
            "name": "SerializerHero123",
            "level": 1,  # Ungültiger Wert für Level
            "experience_points": -1,
        }

        serializer = CharacterSerializer(data=data)
        self.assertFalse(serializer.is_valid())  # Der Serializer sollte invalid sein
        self.assertIn("experience_points", serializer.errors)  # Überprüfe, ob 'level' in den Fehlern ist
