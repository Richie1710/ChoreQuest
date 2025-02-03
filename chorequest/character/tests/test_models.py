"""Module contains unit tests for the character models in the ChoreQuest application."""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from character.models import (
    Character,
    InventoryItem,
    Item,
    SlotChoices,
    calculate_experience_to_next_level,
    calculate_hitpoints_and_mana,
)


class CharacterModelTest(TestCase):
    """Teste die Funktionalität des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_models",
            email="testuser@example.com",
            password="password123",  # noqa: S106
        )

    def test_character_creation(self) -> None:
        """Teste die Erstellung eines Charakters."""
        character = Character.objects.create(
            user=self.user,
            name="TestHero123",
            level=1,
            experience_points=0,
        )

        self.assertEqual(character.user, self.user)
        self.assertEqual(character.name, "TestHero123")
        self.assertEqual(character.level, 1)
        self.assertEqual(character.experience_points, 0)
        self.assertTrue(character.date_created)  # Vergewissere dich, dass das Datum gesetzt wurde

    def test_character_unique_name(self) -> None:
        """Teste, dass der Name eines Charakters einzigartig ist."""
        Character.objects.create(
            user=self.user,
            name="TestHero123",
            level=1,
            experience_points=0,
        )

        with pytest.raises(IntegrityError, match="UNIQUE constraint failed: .*character.*name"):
            Character.objects.create(
                user=self.user,
                name="TestHero123",  # Versuch, denselben Namen erneut zu erstellen
                level=1,
                experience_points=0,
            )

    def test_character_default_values(self) -> None:
        """Teste die Standardwerte für ein Character-Objekt."""
        character = Character.objects.create(
            user=self.user,
            name="Warrior456",
        )

        self.assertEqual(character.level, 1)  # Der Standardwert von `level` sollte 1 sein
        self.assertEqual(character.experience_points, 0)  # Der Standardwert von `experience_points` sollte 0 sein

class CalculateExperienceToNextLevelTest(TestCase):
    """Teste die Funktion calculate_experience_to_next_level."""

    def test_experience_to_next_level_base_case(self) -> None:
        """Teste den Basisfall mit Level 1."""
        self.assertEqual(calculate_experience_to_next_level(1), 100)

    def test_experience_to_next_level_higher_level(self) -> None:
        """Teste die Berechnung für ein höheres Level."""
        self.assertEqual(calculate_experience_to_next_level(5), round(100 * (5 ** 1.5)))

    def test_experience_to_next_level_custom_base_xp(self) -> None:
        """Teste die Berechnung mit einem benutzerdefinierten Basis-XP-Wert."""
        self.assertEqual(calculate_experience_to_next_level(3, base_xp=200), round(200 * (3 ** 1.5)))

    def test_experience_to_next_level_custom_growth_factor(self) -> None:
        """Teste die Berechnung mit einem benutzerdefinierten Wachstumsfaktor."""
        self.assertEqual(calculate_experience_to_next_level(4, growth_factor=2), 100 * (4 ** 2))

class CalculateHitpointsAndManaTest(TestCase):
    """Teste die Funktion calculate_hitpoints_and_mana."""

    def test_hitpoints_and_mana_level_1(self) -> None:
        """Teste die Berechnung für Level 1."""
        hp, mana = calculate_hitpoints_and_mana(1)
        self.assertEqual(hp, 50)
        self.assertEqual(mana, 30)

    def test_hitpoints_and_mana_level_5(self) -> None:
        """Teste die Berechnung für Level 5."""
        hp, mana = calculate_hitpoints_and_mana(5)
        self.assertEqual(hp, round(50 * (1.05 ** 4)))
        self.assertEqual(mana, round(30 * (1.03 ** 4)))

    def test_hitpoints_and_mana_level_10(self) -> None:
        """Teste die Berechnung für Level 10."""
        hp, mana = calculate_hitpoints_and_mana(10)
        self.assertEqual(hp, round(50 * (1.05 ** 9)))
        self.assertEqual(mana, round(30 * (1.03 ** 9)))

class CharacterLevelUpTest(TestCase):
    """Teste die Funktion level_up des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_levelup",
            email="testuser_levelup@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="LevelUpHero",
            level=1,
            experience_points=0,
            experience_points_to_next_level=100,
            hitpoints=50,
            mana=30,
            hitpoints_max=50,
            mana_max=30,
        )

    def test_level_up_increases_level(self) -> None:
        """Teste, ob das Level erhöht wird."""
        self.character.level_up()
        self.assertEqual(self.character.level, 2)

    def test_level_up_resets_experience_points(self) -> None:
        """Teste, ob die Erfahrungspunkte zurückgesetzt werden."""
        self.character.level_up()
        self.assertEqual(self.character.experience_points, 0)

    def test_level_up_updates_experience_points_to_next_level(self) -> None:
        """Teste, ob die Erfahrungspunkte für das nächste Level aktualisiert werden."""
        self.character.level_up()
        self.assertEqual(self.character.experience_points_to_next_level, calculate_experience_to_next_level(2))

    def test_level_up_updates_hitpoints_and_mana(self) -> None:
        """Teste, ob die maximalen HP und MP aktualisiert werden."""
        self.character.level_up()
        expected_hp, expected_mana = calculate_hitpoints_and_mana(2)
        self.assertEqual(self.character.hitpoints_max, expected_hp)
        self.assertEqual(self.character.mana_max, expected_mana)
        self.assertEqual(self.character.hitpoints, expected_hp)
        self.assertEqual(self.character.mana, expected_mana)

class CharacterAddExperienceTest(TestCase):
    """Teste die Funktion add_experience des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_add_experience",
            email="testuser_add_experience@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="ExperienceHero",
            level=1,
            experience_points=0,
            experience_points_to_next_level=100,
            hitpoints=50,
            mana=30,
            hitpoints_max=50,
            mana_max=30,
        )

    def test_add_experience_increases_experience_points(self) -> None:
        """Teste, ob Erfahrungspunkte hinzugefügt werden."""
        self.character.add_experience(50)
        self.assertEqual(self.character.experience_points, 50)

    def test_add_experience_triggers_level_up(self) -> None:
        """Teste, ob ein Level-Up durchgeführt wird, wenn genug Erfahrungspunkte hinzugefügt werden."""
        self.character.add_experience(150)
        self.assertEqual(self.character.level, 2)
        self.assertEqual(self.character.experience_points, 50)  # Restliche XP nach Level-Up

    def test_add_experience_multiple_levels(self) -> None:
        """Teste, ob mehrere Level-Ups durchgeführt werden, wenn genug Erfahrungspunkte hinzugefügt werden."""
        self.character.add_experience(400)
        self.assertEqual(self.character.level, 3)
        self.assertEqual(self.character.experience_points, 17)

    def test_add_experience_no_level_up(self) -> None:
        """Teste, ob kein Level-Up durchgeführt wird, wenn nicht genug Erfahrungspunkte hinzugefügt werden."""
        self.character.add_experience(99)
        self.assertEqual(self.character.level, 1)
        self.assertEqual(self.character.experience_points, 99)

class CharacterStrMethodTest(TestCase):
    """Teste die __str__ Methode des Character-Modells."""

    def setUp(self) -> None:
        """Erstelle einen Benutzer und einen Charakter für den Test."""
        self.user = get_user_model().objects.create_user(
            username="testuser_str",
            email="testuser_str@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="StrHero",
        )

    def test_character_str(self) -> None:
        """Teste die __str__ Methode des Character-Modells."""
        self.assertEqual(str(self.character), "StrHero")

class ItemStrMethodTest(TestCase):
    """Teste die __str__ Methode des Item-Modells."""

    def setUp(self) -> None:
        """Erstelle ein Item für den Test."""
        self.item = Item.objects.create(
            name="TestSword",
            slot=SlotChoices.WEAPON,
            item_type="equipment",
            rarity="rare",
            weight=5.0,
            value=100,
        )

    def test_item_str(self) -> None:
        """Teste die __str__ Methode des Item-Modells."""
        self.assertEqual(str(self.item), "TestSword")

class InventoryItemStrMethodTest(TestCase):
    """Teste die __str__ Methode des InventoryItem-Modells."""

    def setUp(self) -> None:
        """Erstelle einen Benutzer, einen Charakter und ein InventoryItem für den Test."""
        self.user = get_user_model().objects.create_user(
            username="testuser_inventory_str",
            email="testuser_inventory_str@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="InventoryHero",
        )
        self.item = Item.objects.create(
            name="TestShield",
            slot=SlotChoices.SHIELD,
            item_type="equipment",
            rarity="common",
            weight=7.0,
            value=50,
        )
        self.inventory_item = InventoryItem.objects.create(
            character=self.character,
            item=self.item,
            quantity=2,
        )

    def test_inventory_item_str(self) -> None:
        """Teste die __str__ Methode des InventoryItem-Modells."""
        expected_str = "2 x TestShield (Owned by InventoryHero)"
        self.assertEqual(str(self.inventory_item), expected_str)

class CalculateInventoryWeightTest(TestCase):
    """Teste die Funktion calculate_inventory_weight des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_inventory_weight",
            email="testuser_inventory_weight@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="WeightHero",
        )
        self.item1 = Item.objects.create(
            name="TestSword",
            slot=SlotChoices.WEAPON,
            item_type="equipment",
            rarity="rare",
            weight=5.0,
            value=100,
        )
        self.item2 = Item.objects.create(
            name="TestShield",
            slot=SlotChoices.SHIELD,
            item_type="equipment",
            rarity="common",
            weight=7.0,
            value=50,
        )
        self.inventory_item1 = InventoryItem.objects.create(
            character=self.character,
            item=self.item1,
            quantity=2,
        )
        self.inventory_item2 = InventoryItem.objects.create(
            character=self.character,
            item=self.item2,
            quantity=1,
        )

    def test_calculate_inventory_weight(self) -> None:
        """Teste die Berechnung des Inventargewichts."""
        expected_weight = (
            self.item1.weight * self.inventory_item1.quantity
        ) + (
            self.item2.weight * self.inventory_item2.quantity
        )
        self.assertEqual(self.character.calculate_inventory_weight(), expected_weight)

    def test_calculate_inventory_weight_empty(self) -> None:
        """Teste die Berechnung des Inventargewichts, wenn das Inventar leer ist."""
        self.inventory_item1.delete()
        self.inventory_item2.delete()
        self.assertEqual(self.character.calculate_inventory_weight(), 0)

class CharacterHasInventorySpaceTest(TestCase):
    """Teste die Funktion has_inventory_space des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_inventory_space",
            email="testuser_inventory_space@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="SpaceHero",
        )
        self.item1 = Item.objects.create(
            name="TestSword",
            slot=SlotChoices.WEAPON,
            item_type="equipment",
            rarity="rare",
            weight=5.0,
            value=100,
        )
        self.item2 = Item.objects.create(
            name="TestShield",
            slot=SlotChoices.SHIELD,
            item_type="equipment",
            rarity="common",
            weight=7.0,
            value=50,
        )

    def test_has_inventory_space_within_limits(self) -> None:
        """Teste, ob genügend Platz im Inventar ist, wenn die Limits nicht überschritten werden."""
        self.assertTrue(self.character.has_inventory_space(self.item1, quantity=1))

    def test_has_inventory_space_exceeds_slots(self) -> None:
        """Teste, ob genügend Platz im Inventar ist, wenn die Slot-Limits überschritten werden."""
        self.character.max_inventory_slots = 1
        InventoryItem.objects.create(character=self.character, item=self.item1, quantity=1)
        self.assertFalse(self.character.has_inventory_space(self.item2, quantity=1))

    def test_has_inventory_space_exceeds_weight(self) -> None:
        """Teste, ob genügend Platz im Inventar ist, wenn die Gewichtslimits überschritten werden."""
        self.character.max_carry_weight = 5.0
        self.assertFalse(self.character.has_inventory_space(self.item2, quantity=1))

    def test_has_inventory_space_with_multiple_items(self) -> None:
        """Teste, ob genügend Platz im Inventar ist, wenn mehrere Items hinzugefügt werden."""
        InventoryItem.objects.create(character=self.character, item=self.item1, quantity=2)
        self.assertTrue(self.character.has_inventory_space(self.item2, quantity=1))

    def test_has_inventory_space_with_multiple_items_exceeds_weight(self) -> None:
        """Teste, ob das Gewichtslimit überschritten wird, wenn mehrere Items hinzugefügt werden."""
        self.character.max_carry_weight = 10.0
        InventoryItem.objects.create(character=self.character, item=self.item1, quantity=2)
        self.assertFalse(self.character.has_inventory_space(self.item2, quantity=1))

class CharacterAddItemToInventoryTest(TestCase):
    """Teste die Funktion add_item_to_inventory des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_add_item",
            email="testuser_add_item@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="InventoryHero",
        )
        self.item1 = Item.objects.create(
            name="TestSword",
            slot=SlotChoices.WEAPON,
            item_type="equipment",
            rarity="rare",
            weight=5.0,
            value=100,
        )
        self.item2 = Item.objects.create(
            name="TestShield",
            slot=SlotChoices.SHIELD,
            item_type="equipment",
            rarity="common",
            weight=7.0,
            value=50,
        )
        self.item3 = Item.objects.create(
            name="TestPotion",
            slot=SlotChoices.NONE,
            item_type="Consumable",
            rarity="common",
            weight=1.0,
            value=5,
            stacksize=10,
        )

    def test_add_item_to_inventory_success(self) -> None:
        """Teste das Hinzufügen eines Items zum Inventar."""
        self.character.add_item_to_inventory(self.item1, quantity=1)
        inventory_item = InventoryItem.objects.get(character=self.character, item=self.item1)
        self.assertEqual(inventory_item.quantity, 1)

    def test_add_item_to_inventory_existing_item_stacksize1(self) -> None:
        """Teste das Hinzufügen eines Items, das bereits im Inventar vorhanden ist."""
        InventoryItem.objects.create(character=self.character, item=self.item1, quantity=1)
        self.character.add_item_to_inventory(self.item1, quantity=2)
        inventory_item = InventoryItem.objects.filter(character=self.character, item=self.item1)
        self.assertEqual(len(inventory_item), 3)

    def test_add_inital_item_to_inventory_existing_item_under_max_stacksize(self) -> None:
        """Teste das Hinzufügen eines Items unterhalb des Stacklimits."""
        self.character.add_item_to_inventory(self.item3, quantity=5)
        inventory_item = InventoryItem.objects.filter(character=self.character, item=self.item3)
        self.assertEqual(len(inventory_item), 1)
        inventory_item_single = inventory_item.first()
        self.assertEqual(inventory_item_single.quantity, 5)

    def test_add_inital_item_to_inventory_existing_item_over_max_stacksize(self) -> None:
        """Teste das Hinzufügen eines Items, über dem Stack limit."""
        self.character.add_item_to_inventory(self.item3, quantity=18)
        inventory_item = InventoryItem.objects.filter(character=self.character, item=self.item3)
        self.assertEqual(len(inventory_item), 2)
        inventory_item_single = inventory_item.first()
        inventory_item_next = inventory_item[1]
        self.assertEqual(inventory_item_single.quantity, 10)
        self.assertEqual(inventory_item_next.quantity, 8)

    def test_add_item_to_inventory_existing_item_over_stacksize(self) -> None:
        """Teste das Hinzufügen eines Items, das bereits im Inventar vorhanden ist."""
        InventoryItem.objects.create(character=self.character, item=self.item3, quantity=8)
        self.character.add_item_to_inventory(self.item3, quantity=5)
        inventory_item = InventoryItem.objects.filter(character=self.character, item=self.item3)
        self.assertEqual(len(inventory_item), 2)
        inventory_item_single = inventory_item.first()
        inventory_item_next = inventory_item[1]
        self.assertEqual(inventory_item_single.quantity, 10)
        self.assertEqual(inventory_item_next.quantity, 3)

    def test_add_item_to_inventory_existing_item_stacksize_exact(self) -> None:
        """Teste das Hinzufügen eines Items, das bereits im Inventar vorhanden ist."""
        InventoryItem.objects.create(character=self.character, item=self.item3, quantity=10)
        self.character.add_item_to_inventory(self.item3, quantity=5)
        inventory_item = InventoryItem.objects.filter(character=self.character, item=self.item3)
        self.assertEqual(len(inventory_item), 2)
        inventory_item_single = inventory_item.first()
        inventory_item_next = inventory_item[1]
        self.assertEqual(inventory_item_single.quantity, 10)
        self.assertEqual(inventory_item_next.quantity, 5)

    def test_add_item_to_inventory_exceeds_slots(self) -> None:
        """Teste das Hinzufügen eines Items, wenn die Slot-Limits überschritten werden."""
        self.character.max_inventory_slots = 1
        InventoryItem.objects.create(character=self.character, item=self.item1, quantity=1)
        with pytest.raises(ValueError, match="Not enough space or weight capacity in inventory."):
            self.character.add_item_to_inventory(self.item2, quantity=1)

    def test_add_item_to_inventory_exceeds_weight(self) -> None:
        """Teste das Hinzufügen eines Items, wenn die Gewichtslimits überschritten werden."""
        self.character.max_carry_weight = 5.0
        with pytest.raises(ValueError, match="Not enough space or weight capacity in inventory."):
            self.character.add_item_to_inventory(self.item2, quantity=1)

    def test_add_item_to_inventory_multiple_items(self) -> None:
        """"Teste das hinzufügen von mehreren Items zum Inventar."""
        self.character.add_item_to_inventory(self.item1, quantity=2)
        self.character.add_item_to_inventory(self.item2, quantity=1)
        self.character.add_item_to_inventory(self.item3, quantity=5)
        inventory_item1 = InventoryItem.objects.filter(character=self.character, item=self.item1)
        inventory_item2 = InventoryItem.objects.filter(character=self.character, item=self.item2)
        inventory_item3 = InventoryItem.objects.filter(character=self.character, item=self.item3)
        self.assertEqual(len(inventory_item1), 2)
        self.assertEqual(len(inventory_item2), 1)
        self.assertEqual(len(inventory_item3), 1)
        self.assertEqual(inventory_item1[0].quantity, 1)
        self.assertEqual(inventory_item1[1].quantity, 1)
        self.assertEqual(inventory_item2[0].quantity, 1)
        self.assertEqual(inventory_item3[0].quantity, 5)

class CharacterRemoveItemFromInventoryTest(TestCase):
    """Teste die Funktion remove_item_from_inventory des Character-Modells."""

    def setUp(self) -> None:
        """Initialisiere die benötigten Objekte für die Tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser_remove_item",
            email="testuser_remove_item@example.com",
            password="password123",  # noqa: S106
        )
        self.character = Character.objects.create(
            user=self.user,
            name="RemoveItemHero",
        )
        self.item1 = Item.objects.create(
            name="TestSword",
            slot=SlotChoices.WEAPON,
            item_type="equipment",
            rarity="rare",
            weight=5.0,
            value=100,
        )
        self.item2 = Item.objects.create(
            name="TestShield",
            slot=SlotChoices.SHIELD,
            item_type="equipment",
            rarity="common",
            weight=7.0,
            value=50,
        )
        self.inventory_item1 = InventoryItem.objects.create(
            character=self.character,
            item=self.item1,
            quantity=2,
        )
        self.inventory_item2 = InventoryItem.objects.create(
            character=self.character,
            item=self.item2,
            quantity=1,
        )

    def test_remove_item_from_inventory_success(self) -> None:
        """Teste das Entfernen eines Items aus dem Inventar."""
        self.character.remove_item_from_inventory(self.item1, quantity=1)
        inventory_item = InventoryItem.objects.get(character=self.character, item=self.item1)
        self.assertEqual(inventory_item.quantity, 1)

    def test_remove_item_from_inventory_all_quantity(self) -> None:
        """Teste das Entfernen eines Items, wenn die gesamte Menge entfernt wird."""
        self.character.remove_item_from_inventory(self.item2, quantity=1)
        with pytest.raises(InventoryItem.DoesNotExist):
            InventoryItem.objects.get(character=self.character, item=self.item2)

    def test_remove_item_from_inventory_not_enough_quantity(self) -> None:
        """Teste das Entfernen eines Items, wenn nicht genug Menge vorhanden ist."""
        with pytest.raises(ValueError, match="Not enough items to remove."):
            self.character.remove_item_from_inventory(self.item1, quantity=3)

    def test_remove_item_from_inventory_item_not_found(self) -> None:
        """Teste das Entfernen eines Items, das nicht im Inventar vorhanden ist."""
        self.item3 = Item.objects.create(
            name="NotExistingSword",
            slot=SlotChoices.SHIELD,
            item_type="equipment",
            rarity="common",
            weight=7.0,
            value=50,
        )
        with pytest.raises(ValueError, match="Item not found in inventory."):
            self.character.remove_item_from_inventory(self.item3, quantity=2)
