"""Inits the tests for user module."""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chorequest.settings")
django.setup()
