"""
Migration script to add the 'active' field to the 'character' model.

Generated by Django 5.1.4 on 2024-12-18 08:48.
"""

from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration to add the 'active' field to the 'character' model."""

    dependencies: ClassVar[list] = [
        ("character", "0004_character_experience_points_to_next_level"),
    ]

    operations: ClassVar[list] = [
        migrations.AddField(
            model_name="character",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]
