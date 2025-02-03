"""Module contains the configuration for the Character app."""

from django.apps import AppConfig


class CharacterConfig(AppConfig):
    """Configuration for the Character app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "character"
