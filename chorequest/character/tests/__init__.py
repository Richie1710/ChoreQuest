"""Initializes the Django environment for the tests for charatcer module."""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chorequest.settings")
django.setup()
