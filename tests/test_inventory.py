from inventory import (
    format_item,
    next_number,
    normalize_item,
    add_item,
    find_by_number,
    find_by_room,
    update_item,
    delete_item,
)
from storage import load_items


def make_item(number="INV-0001", room="204", status="исправно"):
    return {
        "inv_number": number,
        "type": "ПК",
        "name": "ПК",
        "room": room,
        "status": status,
    }


def test_demo_data():
    assert len(load_items()) >= 5


def test_add_ok():
    items = []
    assert add_item(items, make_item()) is None
    assert len(items) == 1


def test_add_empty():
    items = []
    data = {"inv_number": "", "type": "", "name": "",
            "room": "", "status": ""}
    assert add_item(items, data) is not None
    assert len(items) == 0


def test_add_duplicate():
    items = [make_item()]
    assert add_item(items, make_item()) is not None
    assert len(items) == 1


def test_next_number():
    assert next_number([{"inv_number": "INV-0003"}]) == "INV-0004"


def test_format():
    text = format_item(make_item())
    assert "INV-0001" in text
    assert "каб. 204" in text


def test_find_by_number_ok():
    items = [make_item("INV-0001"), make_item("INV-0002")]
    assert find_by_number(items, "INV-0002")["inv_number"] == "INV-0002"


def test_find_by_number_missing():
    assert find_by_number([make_item()], "INV-9999") is None


def test_find_by_room():
    items = [make_item("INV-0001", room="204"),
             make_item("INV-0002", room="205"),
             make_item("INV-0003", room="204")]
    assert len(find_by_room(items, "204")) == 2
    assert find_by_room(items, "999") == []


def test_update_ok():
    items = [make_item()]
    assert update_item(items, "INV-0001", room="301", status="списано") is None
    assert items[0]["room"] == "301"
    assert items[0]["status"] == "списано"


def test_update_missing():
    assert update_item([], "INV-9999", room="301") == "Запись не найдена."


def test_update_bad_status():
    items = [make_item()]
    assert update_item(items, "INV-0001", status="сломано") is not None


def test_delete_ok():
    items = [make_item()]
    assert delete_item(items, "INV-0001") is None
    assert items == []


def test_delete_missing():
    assert delete_item([], "INV-9999") == "Запись не найдена."


def test_normalize_fills_missing_fields():
    item = normalize_item({"inv_number": " INV-0001 "})
    assert item["inv_number"] == "INV-0001"
    assert item["room"] == ""
    assert set(item) == {"inv_number", "type", "name", "room",
                         "status", "date_added", "responsible"}


def test_format_handles_incomplete_item():
    text = format_item({"inv_number": "INV-0009"})
    assert "INV-0009" in text
    assert "каб." in text