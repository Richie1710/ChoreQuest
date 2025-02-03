"""
Module: quest.models.

Filepath: ChoreQuest/chorequest/quest/models.py.

This module defines the models for the Quest system in the ChoreQuest application.
It includes the following models:

- Quest: Represents a task or activity that needs to be completed.
- CharacterQuest: Tracks the relationship between a character and a quest.
- QuestReward: Defines the rewards for completing a quest.
- QuestRewardItemLoot: Defines specific item loot for a quest reward.
- LootTable: Defines conditions for advanced loot logic.

Each model includes fields and methods relevant to its purpose within the quest system.
"""

from django.db import models
from django.utils import timezone


class Quest(models.Model):
    """Represents a task or activity that needs to be completed."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)  # Aktiv/Deaktiviert
    experience_points = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    item_loot = models.ManyToManyField("QuestRewardItemLoot", blank=True)

    def __str__(self) -> str:
        """Return a string representation of the Quest."""
        return self.name

    def is_overdue(self) -> bool:
        """Check if the quest is overdue."""
        return self.due_date < timezone.now()


class CharacterQuest(models.Model):
    """Tracks the relationship between a character and a quest."""

    character = models.ForeignKey("character.Character", on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[("open", "Open"), ("accepted", "Accepted"), ("completed", "Completed")],
        default="open",
    )
    progress = models.IntegerField(default=0)  # Fortschritt (0-100%)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta information for CharacterQuest model."""

        unique_together = ("character", "quest")

    def __str__(self) -> str:
        """Return a string representation of the CharacterQuest."""
        return f"{self.character.name} - {self.quest.name} ({self.status})"


class QuestRewardItemLoot(models.Model):
    """Defines specific item loot for a quest reward."""

    item = models.ForeignKey("character.Item", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    probability = models.FloatField(help_text="Probability of this loot being awarded (0.0 - 1.0)")

    def __str__(self) -> str:
        """Return a string representation of the QuestRewardItemLoot."""
        return f"{self.item.name} x{self.quantity} ({self.probability * 100}%)"


class LootTable(models.Model):
    """Defines conditions for advanced loot logic."""

    name = models.CharField(max_length=255)
    conditions = models.TextField(help_text="Conditions as JSON or DSL for advanced loot logic.")
    rewards = models.ManyToManyField(QuestRewardItemLoot)

    def __str__(self) -> str:
        """Return a string representation of the LootTable."""
        return self.name
