"""
Admin configuration for the quest-related models in the ChoreQuest application.

This module provides the admin interface for managing quests, character quests, quest rewards,
quest reward item loots, and loot tables.

Filepath: ChoreQuest/chorequest/quest/admin.py

Classes:
    QuestAdmin: Admin configuration for the Quest model.
    CharacterQuestAdmin: Admin configuration for the CharacterQuest model.
    QuestRewardAdmin: Admin configuration for the QuestReward model.
    QuestRewardItemLootAdmin: Admin configuration for the QuestRewardItemLoot model.
    LootTableAdmin: Admin configuration for the LootTable model.
"""

from django.contrib import admin

from .models import CharacterQuest, LootTable, Quest, QuestRewardItemLoot


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    """Admin configuration for the Quest model."""

    list_display = ("name", "due_date", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "due_date", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    date_hierarchy = "due_date"


@admin.register(CharacterQuest)
class CharacterQuestAdmin(admin.ModelAdmin):
    """Admin configuration for the CharacterQuest model."""

    list_display = ("character", "quest", "status", "progress", "accepted_at", "completed_at")
    list_filter = ("status", "accepted_at", "completed_at")
    search_fields = ("character__name", "quest__name")
    ordering = ("-accepted_at",)


@admin.register(QuestRewardItemLoot)
class QuestRewardItemLootAdmin(admin.ModelAdmin):
    """Admin configuration for the QuestRewardItemLoot model."""

    list_display = ("item", "quantity", "probability")
    list_filter = ("item",)
    search_fields = ("item__name",)


@admin.register(LootTable)
class LootTableAdmin(admin.ModelAdmin):
    """Admin configuration for the LootTable model."""

    list_display = ("name",)
    search_fields = ("name", "conditions")
    filter_horizontal = ("rewards",)
