"""
Module: quest.tests.test_models.

Filepath: ChoreQuest/chorequest/quest/tests/test_models.py.
Tests for the Quest model.
"""


import datetime

from django.test import TestCase
from django.utils import timezone

from quest.factories import QuestFactory


class QuestModelTests(TestCase):
    """Tests for the Quest model."""

    def setUp(self) -> None:
        """Set up a test quest using QuestFactory."""
        self.TEST_EXPERIENCE_POINTS = 100
        self.TEST_GOLD = 50
        self.quest = QuestFactory(
            name="Test Quest",
            description="A test quest",
            due_date=timezone.now() + datetime.timedelta(days=1),
            experience_points=self.TEST_EXPERIENCE_POINTS,
            gold=self.TEST_GOLD,
        )

    def test_string_representation(self) -> None:
        """Test the string representation of the Quest model."""
        self.assertEqual(str(self.quest), "Test Quest")

    def test_is_overdue(self) -> None:
        """Test the is_overdue method."""
        # Set the due_date in the past and check
        self.quest.due_date = timezone.now() - datetime.timedelta(days=1)
        self.quest.save()
        self.assertTrue(self.quest.is_overdue())

        # Set the due_date in the future and check
        self.quest.due_date = timezone.now() + datetime.timedelta(days=1)
        self.quest.save()
        self.assertFalse(self.quest.is_overdue())

    def test_default_values(self) -> None:
        """Test default values for a quest."""
        self.assertEqual(self.quest.experience_points, self.TEST_EXPERIENCE_POINTS)
        self.assertEqual(self.quest.gold, self.TEST_GOLD)
        self.assertEqual(self.quest.item_loot.count(), 0)
