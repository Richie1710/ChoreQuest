"""Module contains the configuration for the User app."""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """Configuration for the User app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
