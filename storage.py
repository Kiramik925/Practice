import json
from datetime import datetime
from pathlib import Path

from inventory import normalize_item

DATA_FILE = Path(__file__).resolve().parent / "data" / "inventory.json"
LAST_MESSAGE = None


def last_message():
    return LAST_MESSAGE


def _target(path):
    return Path(path) if path else DATA_FILE


def _backup(path):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.corrupt-{stamp}")
    try:
        backup.write_bytes(path.read_bytes())
    except OSError:
        return None
    return backup


def load_items(path=None):
    global LAST_MESSAGE
    LAST_MESSAGE = None
    file = _target(path)

    if not file.exists():
        LAST_MESSAGE = "Файл данных не найден. Он будет создан при первом сохранении."
        return []

    try:
        raw = file.read_text(encoding="utf-8")
    except OSError:
        LAST_MESSAGE = f"Файл {file.name} не удалось прочитать."
        return []

    if not raw.strip():
        LAST_MESSAGE = f"Файл {file.name} пуст. Список оборудования пуст."
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        backup = _backup(file)
        LAST_MESSAGE = _corrupt_message(file, backup)
        return []

    if not isinstance(data, list):
        backup = _backup(file)
        LAST_MESSAGE = _corrupt_message(file, backup)
        return []

    items = [normalize_item(record) for record in data if isinstance(record, dict)]
    skipped = len(data) - len(items)
    if skipped:
        LAST_MESSAGE = f"В файле {file.name} пропущено некорректных записей: {skipped}."
    return items


def save_items(items, path=None):
    file = _target(path)
    text = json.dumps([normalize_item(item) for item in items], ensure_ascii=False, indent=2)
    temp = file.with_name(file.name + ".tmp")
    try:
        file.parent.mkdir(parents=True, exist_ok=True)
        temp.write_text(text, encoding="utf-8")
        temp.replace(file)
    except OSError:
        return f"Не удалось сохранить данные в {file.name}."
    return None


def _corrupt_message(file, backup):
    if backup is None:
        return f"Файл {file.name} повреждён и не читается. Копию сохранить не удалось, список начат пустым."
    return f"Файл {file.name} повреждён. Копия сохранена как {backup.name}, список начат пустым."
