import json

from storage import load_items, save_items, last_message


def make_item(number="INV-0001", room="204", status="исправно"):
    return {
        "inv_number": number,
        "type": "ПК",
        "name": "Системный блок",
        "room": room,
        "status": status,
        "date_added": "2024-09-01",
        "responsible": "Иванов И.И.",
    }


def test_save_creates_file_and_directory(data_dir):
    path = data_dir / "data" / "inventory.json"
    save_items([make_item()], path)
    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8"))[0]["inv_number"] == "INV-0001"


def test_save_and_load_round_trip(data_dir):
    path = data_dir / "inventory.json"
    items = [make_item(), make_item("INV-0002", room="205")]
    save_items(items, path)
    loaded = load_items(path)
    assert len(loaded) == 2
    assert loaded[1]["room"] == "205"


def test_cyrillic_survives_round_trip(data_dir):
    path = data_dir / "inventory.json"
    save_items([make_item()], path)
    loaded = load_items(path)
    assert loaded[0]["name"] == "Системный блок"
    assert loaded[0]["status"] == "исправно"


def test_load_missing_file_returns_empty(data_dir):
    items = load_items(data_dir / "нет-файла.json")
    assert items == []
    assert "не найден" in last_message()


def test_load_empty_file_returns_empty(data_dir):
    path = data_dir / "inventory.json"
    path.write_text("   \n", encoding="utf-8")
    assert load_items(path) == []
    assert "пуст" in last_message()


def test_load_corrupt_json_makes_backup(data_dir):
    path = data_dir / "inventory.json"
    path.write_text('{"inv_number": "INV-0001",', encoding="utf-8")
    assert load_items(path) == []
    backups = list(data_dir.glob("inventory.json.corrupt-*"))
    assert len(backups) == 1
    assert "повреждён" in last_message()


def test_load_non_list_json_makes_backup(data_dir):
    path = data_dir / "inventory.json"
    path.write_text('{"items": []}', encoding="utf-8")
    assert load_items(path) == []
    assert list(data_dir.glob("inventory.json.corrupt-*"))


def test_load_skips_broken_records(data_dir):
    path = data_dir / "inventory.json"
    path.write_text(json.dumps([make_item(), 7, "текст"]), encoding="utf-8")
    loaded = load_items(path)
    assert len(loaded) == 1
    assert "пропущено" in last_message()


def test_load_fills_missing_fields(data_dir):
    path = data_dir / "inventory.json"
    path.write_text(json.dumps([{"inv_number": "INV-0001"}]), encoding="utf-8")
    loaded = load_items(path)
    assert loaded[0]["type"] == ""
    assert loaded[0]["responsible"] == ""


def test_save_leaves_no_temp_file(data_dir):
    path = data_dir / "inventory.json"
    save_items([make_item()], path)
    assert list(data_dir.glob("*.tmp")) == []


def test_save_overwrites_previous_content(data_dir):
    path = data_dir / "inventory.json"
    save_items([make_item(), make_item("INV-0002")], path)
    save_items([make_item("INV-0003")], path)
    loaded = load_items(path)
    assert [item["inv_number"] for item in loaded] == ["INV-0003"]
