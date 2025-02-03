"""Serializers for the character app."""

from typing import Any, ClassVar

from rest_framework import serializers

from .models import Character, InventoryItem, Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer für die Item-Daten."""

    class Meta:
        """Meta class for ItemSerializer."""

        model = Item
        fields: ClassVar[list[str]] = ["id", "name", "description", "stacksize", "weight", "icon"]

    def get_icon_url(self, obj: Item) -> "str | None":
        """Return the URL of the icon image or None if no icon is available."""
        request = self.context.get("request")
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer für die InventoryItem-Daten."""

    item = ItemSerializer()  # Ein verschachtelter Serializer für das Item

    class Meta:
        """Meta class for InventoryItemSerializer."""

        model = InventoryItem
        fields: ClassVar[list[str]] = ["id", "item", "quantity"]  # Die Inventarinfos

class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for the Character model."""

    inventory = InventoryItemSerializer(many=True, required=False)

    class Meta:
        """Meta class for CharacterSerializer."""

        model = Character
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "level",
            "experience_points",
            "user",
            "experience_points_to_next_level",
            "strength",
            "dexterity",
            "intelligence",
            "constitution",
            "wisdom",
            "charisma",
            "date_created",
            "hitpoints",
            "mana",
            "hitpoints_max",
            "mana_max",
            "inventory",
        ]
        extra_kwargs: ClassVar[dict] = {"user": {"required": False}}

    def validate_level(self, value:int) -> int:
        """Validiert, dass der Level immer größer als 0 ist."""
        if value < 0:
            msg = "Level must be a positive integer."
            raise serializers.ValidationError(msg)
        return value

    def validate_experience(self, value: int) -> int:
        """Validiert, dass der Experiance immer größer als 0 ist."""
        if value < 0:
            msg = "Level must be a positive integer."
            raise serializers.ValidationError(msg)
        return value


    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validiert die Daten des Characters.

        Der Level muss immer größer als 0 sein.
        Die Erfahrungspunkte müssen immer größer oder gleich 0 sein.
        """
        if data["level"] <= 0:
            raise serializers.ValidationError({"level": "Level must be a positive integer."})

        if data["experience_points"] < 0:
            raise serializers.ValidationError({"experience_points": "Experience points must be a positive integer."})
        return data

    def create(self, validated_data: dict[str, Any]) -> Character:
        """Create a new Character instance with the provided validated data."""
        inventory_data = validated_data.pop("inventory", [])
        character = super().create(validated_data)

        for item_data in inventory_data:
            InventoryItem.objects.create(character=character, **item_data)
        return character
