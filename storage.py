"""Хранение данных в JSON (Спринт 1 — только загрузка демо-данных)."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "inventory.json"


def load_items():
    """Загружает записи из файла. Если файла нет — пустой список."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_items(items):
    """Сохраняет записи в файл (понадобится в Спринте 4)."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
