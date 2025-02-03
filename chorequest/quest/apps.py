"""
Module: quest.apps.

Filepath: ChoreQuest/chorequest/quest/apps.py.


This module contains the configuration for the quest app.
"""

from django.apps import AppConfig


class QuestConfig(AppConfig):
    """Configuration for the quest app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "quest"
