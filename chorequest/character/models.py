"""Module containing the models for characters, items, and inventory in the ChoreQuest game."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices


class SlotChoices(TextChoices):
    """Enumeration for different equipment slots."""

    HEAD = "head", "Head"
    CHEST = "chest", "Chest"
    LEGS = "legs", "Legs"
    WEAPON = "weapon", "Weapon"
    SHIELD = "shield", "Shield"
    RING = "ring", "Ring"
    NECKLACE = "necklace", "Necklace"
    BOOTS = "boots", "Boots"
    GLOVES = "gloves", "Gloves"
    NONE = "none", "None"


class Item(models.Model):
    """Item model representing an item."""

    name = models.CharField(max_length=100, unique=True)
    slot = models.CharField(max_length=20, choices=SlotChoices.choices, default=SlotChoices.NONE)
    item_type = models.CharField(
        max_length=20,
        choices=[("consumable", "Consumable"), ("equipment", "Equipment"), ("quest", "Quest Item")],
        default="equipment",
    )
    rarity = models.CharField(
        max_length=20,
        choices=[
            ("trash", "Trash"),
            ("common", "Common"),
            ("rare", "Rare"),
            ("epic", "Epic"),
            ("legendary", "Legendary"),
        ],
        default="common",
    )
    description = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    value = models.IntegerField(default=0)
    stacksize = models.PositiveIntegerField(default=1)

    current_durability = models.PositiveIntegerField(default=100)
    max_durability = models.PositiveIntegerField(default=100)
    is_repairable = models.BooleanField(default=False)

    strength_bonus = models.IntegerField(default=0)
    dexterity_bonus = models.IntegerField(default=0)
    intelligence_bonus = models.IntegerField(default=0)
    constitution_bonus = models.IntegerField(default=0)
    wisdom_bonus = models.IntegerField(default=0)
    charisma_bonus = models.IntegerField(default=0)
    hitpoints_bonus = models.IntegerField(default=0)
    mana_bonus = models.IntegerField(default=0)

    required_level = models.PositiveIntegerField(default=1)

    icon = models.ImageField(upload_to="item_icons/", blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the string representation of the item."""
        return self.name

def calculate_experience_to_next_level(level: int, base_xp: int = 100, growth_factor: float = 1.5) -> int:
    """Berechnet die benötigten Erfahrungspunkte für das nächste Level basierend auf exponentiellem Wachstum."""
    return round(base_xp * (level ** growth_factor))

def calculate_hitpoints_and_mana(level: int) -> tuple[int, int]:
    """
    Berechnet die maximalen Hitpoints und Mana für das nächste Level.

    Es hat einen exponentiellen Wachstumsfaktor, aber langsamer als XP.
    """
    base_hp = 50  # Basis-HP bei Level 1
    base_mana = 30  # Basis-MP bei Level 1
    hp_growth_factor = 1.05  # Langsame Wachstumsrate von 5% pro Level
    mana_growth_factor = 1.03  # Langsame Wachstumsrate von 3% pro Level

    hp = base_hp * (hp_growth_factor ** (level - 1))
    mana = base_mana * (mana_growth_factor ** (level - 1))

    return round(hp), round(mana)

class Character(models.Model):
    """Character model representing a game character associated with a user."""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Verknüpft den Charakter mit dem Benutzer
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    experience_points_to_next_level = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    hitpoints = models.IntegerField(default=10)
    mana = models.IntegerField(default=10)
    hitpoints_max = models.IntegerField(default=10)
    mana_max = models.IntegerField(default=10)
    max_inventory_slots = models.IntegerField(default=20)
    max_carry_weight = models.FloatField(default=50.0)

    def __str__(self) -> str:
        """Return the string representation of the character."""
        return self.name

    def level_up(self) -> None:
        """
        Erhöht das Level des Charakters, basierend auf den Erfahrungspunkten.

        Erhöht die maximalen Erfahrungspunkte und passt HP und MP an.
        """
        # Level erhöhen
        self.level += 1

        # Erfahrungspunkte anpassen
        self.experience_points = 0

        # Berechne die maximalen Erfahrungspunkte für das nächste Level
        self.experience_points_to_next_level = calculate_experience_to_next_level(self.level)

        # HP und MP bei jedem Level-Up erhöhen
        hp, mana = calculate_hitpoints_and_mana(self.level)
        self.hitpoints_max = hp
        self.mana_max = mana

        # Die aktuellen Werte für HP und MP (die eigentlichen Punkte des Charakters)
        self.hitpoints = self.hitpoints_max
        self.mana = self.mana_max

        # Speichern des Charakters
        self.save()

    def calculate_inventory_weight(self) -> int:
        """Berechnet das aktuelle Gewicht aller Items im Inventar."""
        return sum(item.item.weight * item.quantity for item in self.inventory.all())

    def has_inventory_space(self, new_item: Item, quantity: int=1) -> bool:
        """Überprüft, ob genügend Platz im Inventar ist (Slots und Gewicht)."""
        # Check Slot Space
        if self.inventory.count() >= self.max_inventory_slots:
            return False
        # Check Weight
        current_weight = self.calculate_inventory_weight()
        additional_weight = new_item.weight * quantity
        return not Decimal(current_weight) + Decimal(additional_weight) > Decimal(self.max_carry_weight)

    def add_item_to_inventory(self, item: Item, quantity:int=1) -> None:
        """Fügt ein Item zum Inventar hinzu, unter Berücksichtigung von Stacklimits und Platzkapazität."""
        if not self.has_inventory_space(item, quantity):
            msg = "Not enough space or weight capacity in inventory."
            raise ValueError(msg)

        stack_limit = item.stacksize
        remaining_quantity = quantity

        # Überprüfe, ob das Item bereits existiert
        existing_inventory_items = InventoryItem.objects.filter(character=self, item=item)

        for inventory_item in existing_inventory_items:
            # Berechne freien Platz in diesem Stack
            available_space = stack_limit - inventory_item.quantity

            if available_space > 0:
                # Füge so viel wie möglich zu diesem Stack hinzu
                added_quantity = min(available_space, remaining_quantity)
                inventory_item.quantity += added_quantity
                inventory_item.save()
                remaining_quantity -= added_quantity

            # Wenn keine Menge mehr übrig ist, können wir abbrechen
            if remaining_quantity <= 0:
                return

        # Falls noch nicht alles hinzugefügt wurde, erstelle neue Stacks
        while remaining_quantity > 0:
            # Neue Stackmenge ist entweder das Restlimit oder die verbleibende Menge
            stack_quantity = min(stack_limit, remaining_quantity)
            InventoryItem.objects.create(character=self, item=item, quantity=stack_quantity)
            remaining_quantity -= stack_quantity


    def remove_item_from_inventory(self, item:Item, quantity:int=1)->None:
        """Entfernt ein Item aus dem Inventar."""
        inventory_item = InventoryItem.objects.filter(character=self, item=item).first()
        if not inventory_item:
            msg = "Item not found in inventory."
            raise ValueError(msg)

        if inventory_item.quantity < quantity:
            msg = "Not enough items to remove."
            raise ValueError(msg)

        inventory_item.quantity -= quantity
        if inventory_item.quantity == 0:
            inventory_item.delete()
        else:
            inventory_item.save()

    def add_experience(self, points: int) -> None:
        """Fügt dem Charakter Erfahrungspunkte hinzu und prüft, ob er leveln sollte."""
        self.experience_points += points

        # Überprüfe, ob genug Erfahrung für das nächste Level vorhanden ist
        while self.experience_points >= self.experience_points_to_next_level:
            # Berechne die verbleibenden Erfahrungspunkte nach dem Level-Up
            left_over_xp = self.experience_points - self.experience_points_to_next_level

            # Level-Up durchführen
            self.level_up()

            # Setze die verbleibenden XP nach dem Level-Up
            self.experience_points = left_over_xp





class InventoryItem(models.Model):
    """Represents an item in a character's inventory."""

    character = models.ForeignKey("Character", on_delete=models.CASCADE, related_name="inventory")
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    current_durability = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        """Return the string representation of the inventory item."""
        return f"{self.quantity} x {self.item.name} (Owned by {self.character.name})"
