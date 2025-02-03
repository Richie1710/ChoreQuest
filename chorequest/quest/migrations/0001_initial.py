"""Module containing the initial migration for the quest app models."""

from typing import ClassVar

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Initial migration for the quest app models."""

    initial = True

    dependencies: ClassVar[list] = [
        ("character", "0006_item_character_max_carry_weight_and_more"),
    ]

    operations: ClassVar[list] = [
        migrations.CreateModel(
            name="QuestRewardItemLoot",  # Hinzugefügt, um den Fehler zu beheben
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "probability",
                    models.FloatField(
                        help_text="Probability of this loot being awarded (0.0 - 1.0)",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="character.item",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Quest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("due_date", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                ("experience_points", models.IntegerField(default=0)),
                ("gold", models.IntegerField(default=0)),
                (
                    "item_loot",
                    models.ManyToManyField(blank=True, to="quest.questrewarditemloot"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LootTable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "conditions",
                    models.TextField(
                        help_text="Conditions as JSON or DSL for advanced loot logic.",
                    ),
                ),
                ("rewards", models.ManyToManyField(to="quest.questrewarditemloot")),
            ],
        ),
        migrations.CreateModel(
            name="CharacterQuest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("open", "Open"),
                            ("accepted", "Accepted"),
                            ("completed", "Completed"),
                        ],
                        default="open",
                        max_length=50,
                    ),
                ),
                ("progress", models.IntegerField(default=0)),
                ("accepted_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="character.character",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quest.quest",
                    ),
                ),
            ],
            options={
                "unique_together": {("character", "quest")},
            },
        ),
    ]
