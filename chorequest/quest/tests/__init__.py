"""
Module: quest.tests.__init__.

Filepath: ChoreQuest/chorequest/quest/tests/__init__.py.
This package contains tests for the chorequest application.
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chorequest.settings")
django.setup()
