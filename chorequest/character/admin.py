"""Admin configuration for the character app."""

from django.contrib import admin

from .models import Character, InventoryItem, Item


class InventoryItemInline(admin.TabularInline):
    """Inline admin interface for InventoryItem."""

    model = InventoryItem
    extra = 1  # Anzahl leerer Felder für neue Einträge
    fields = ("item", "quantity", "current_durability")

class CharacterAdmin(admin.ModelAdmin):
    """Admin interface for Character."""

    list_display = ("name", "user", "level", "experience_points", "date_created")
    search_fields = ("name", "user__username")
    list_filter = ("level", "experience_points")

admin.site.register(Character, CharacterAdmin)
admin.site.register(Item)
admin.site.register(InventoryItem)
