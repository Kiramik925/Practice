"""Автотесты Спринта 1 (первые 3 тест-кейса)."""

from inventory import format_item
from storage import load_items


def test_format_item():
    """T-01: запись форматируется в строку с номером и кабинетом."""
    item = {
        "inv_number": "INV-0001",
        "type": "ПК",
        "name": "Компьютер",
        "room": "204",
        "status": "исправно",
    }
    text = format_item(item)
    assert "INV-0001" in text
    assert "каб. 204" in text


def test_demo_data_has_at_least_five_records():
    """T-02: демонстрационные данные содержат не менее 5 записей."""
    assert len(load_items()) >= 5


def test_demo_inv_numbers_are_unique():
    """T-03: инвентарные номера в демо-данных уникальны."""
    numbers = [r["inv_number"] for r in load_items()]
    assert len(numbers) == len(set(numbers))
