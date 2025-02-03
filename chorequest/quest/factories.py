"""
Factories for quest models using factory_boy.

This module defines factories for creating test instances of the Quest-related models.
"""

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from quest.models import CharacterQuest, Quest


class QuestFactory(DjangoModelFactory):
    """Factory for Quest model."""

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    due_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=7))
    is_active = factory.Faker("boolean")
    experience_points = factory.Faker("random_int", min=50, max=500)
    gold = factory.Faker("random_int", min=10, max=100)

    class Meta:
        """Meta information for the QuestFactory."""

        model = Quest


class CharacterQuestFactory(DjangoModelFactory):
    """Factory for CharacterQuest model."""

    character = factory.SubFactory("character.factories.CharacterFactory")  # Verweis auf die Character-Factory
    quest = factory.SubFactory(QuestFactory)
    status = factory.Faker("random_element", elements=["open", "accepted", "completed"])
    progress = factory.Faker("random_int", min=0, max=100)
    accepted_at = factory.LazyAttribute(
        lambda obj: timezone.now() if obj.status in ["accepted", "completed"] else None,
    )
    completed_at = factory.LazyAttribute(
        lambda obj: timezone.now() + timezone.timedelta(days=1) if obj.status == "completed" else None,
    )

    class Meta:
        """Meta information for the CharacterQuestFactory."""

        model = CharacterQuest
