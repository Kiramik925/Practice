from inventory import (
    STATUSES,
    add_item,
    delete_item,
    filter_items,
    find_by_number,
    format_item,
    next_number,
    normalize_item,
    update_item,
    validate_number,
    validate_room,
    validate_status,
)
from storage import load_items


def make_item(number="INV-0001", room="204", status="исправно", name="Системный блок"):
    return {
        "inv_number": number,
        "type": "ПК",
        "name": name,
        "room": room,
        "status": status,
        "date_added": "2024-09-01",
        "responsible": "Иванов И.И.",
    }


def test_demo_data():
    assert len(load_items()) >= 5


def test_add_ok():
    items = []
    assert add_item(items, make_item()) is None
    assert len(items) == 1


def test_add_empty():
    items = []
    data = {"inv_number": "", "type": "", "name": "", "room": "", "status": ""}
    assert add_item(items, data) is not None
    assert items == []


def test_add_duplicate():
    items = [make_item()]
    assert add_item(items, make_item()) is not None
    assert len(items) == 1


def test_add_duplicate_in_other_case():
    items = [make_item("INV-0001")]
    assert add_item(items, make_item("inv-0001")) is not None
    assert len(items) == 1


def test_add_keeps_number_in_upper_case():
    items = []
    assert add_item(items, make_item("inv-0007")) is None
    assert items[0]["inv_number"] == "INV-0007"


def test_add_stores_all_fields():
    items = []
    add_item(items, make_item())
    assert set(items[0]) == {"inv_number", "type", "name", "room",
                             "status", "date_added", "responsible"}


def test_next_number():
    assert next_number([{"inv_number": "INV-0003"}]) == "INV-0004"


def test_next_number_ignores_broken_values():
    items = [{"inv_number": "INV-0002"}, {"inv_number": "ABC"}, {"inv_number": "INV-XYZ"}]
    assert next_number(items) == "INV-0003"


def test_next_number_without_items():
    assert next_number([]) == "INV-0001"


def test_format():
    text = format_item(make_item())
    assert "INV-0001" in text
    assert "каб. 204" in text


def test_format_handles_incomplete_item():
    text = format_item({"inv_number": "INV-0009"})
    assert "INV-0009" in text
    assert "каб." in text


def test_normalize_fills_missing_fields():
    item = normalize_item({"inv_number": " INV-0001 "})
    assert item["inv_number"] == "INV-0001"
    assert item["room"] == ""
    assert set(item) == {"inv_number", "type", "name", "room",
                         "status", "date_added", "responsible"}


def test_validate_number_bad_format():
    assert validate_number("1234") is not None
    assert validate_number("INV-12A") is not None


def test_validate_number_empty():
    assert validate_number("") is not None


def test_validate_room_not_digits():
    assert validate_room("2a4") is not None
    assert validate_room("") is not None


def test_validate_status_bad():
    assert validate_status("сломано") is not None
    assert all(validate_status(status) is None for status in STATUSES)


def test_find_by_number_ok():
    items = [make_item("INV-0001"), make_item("INV-0002")]
    assert find_by_number(items, "INV-0002")["inv_number"] == "INV-0002"


def test_find_by_number_ignores_case_and_spaces():
    items = [make_item("INV-0005")]
    assert find_by_number(items, " inv-0005 ")["inv_number"] == "INV-0005"


def test_find_by_number_missing():
    assert find_by_number([make_item()], "INV-9999") is None


def test_find_by_number_empty():
    assert find_by_number([make_item()], "") is None


def test_filter_by_room():
    items = [make_item("INV-0001", room="204"),
             make_item("INV-0002", room="205"),
             make_item("INV-0003", room="204")]
    assert len(filter_items(items, room="204")) == 2
    assert filter_items(items, room="999") == []


def test_filter_by_status():
    items = [make_item(status="исправно"),
             make_item("INV-0002", status="списано"),
             make_item("INV-0003", status="списано")]
    assert len(filter_items(items, status="списано")) == 2


def test_filter_by_room_and_status():
    items = [make_item("INV-0001", room="204", status="исправно"),
             make_item("INV-0002", room="204", status="списано"),
             make_item("INV-0003", room="205", status="списано")]
    found = filter_items(items, room="204", status="списано")
    assert [item["inv_number"] for item in found] == ["INV-0002"]


def test_filter_without_conditions_returns_all():
    items = [make_item(), make_item("INV-0002")]
    assert len(filter_items(items)) == 2
    assert len(filter_items(items, room="", status=None)) == 2


def test_filter_skips_incomplete_items():
    items = [{"inv_number": "INV-0001"}, make_item("INV-0002", room="204")]
    assert filter_items(items, room="204") == [items[1]]


def test_update_ok():
    items = [make_item()]
    assert update_item(items, "INV-0001", room="301", status="списано") is None
    assert items[0]["room"] == "301"
    assert items[0]["status"] == "списано"


def test_update_keeps_other_fields():
    items = [make_item()]
    update_item(items, "INV-0001", room="301")
    assert items[0]["name"] == "Системный блок"
    assert items[0]["status"] == "исправно"


def test_update_missing():
    assert update_item([], "INV-9999", room="301") == "Запись не найдена."


def test_update_bad_status():
    items = [make_item()]
    assert update_item(items, "INV-0001", status="сломано") is not None
    assert items[0]["status"] == "исправно"


def test_update_bad_room():
    items = [make_item()]
    assert update_item(items, "INV-0001", room="2a4") is not None
    assert items[0]["room"] == "204"


def test_delete_ok():
    items = [make_item()]
    assert delete_item(items, "INV-0001") is None
    assert items == []


def test_delete_missing():
    assert delete_item([], "INV-9999") == "Запись не найдена."
