STATUSES = ("исправно", "требует ремонта", "списано")
TYPES = ("ПК", "Монитор", "Принтер", "Ноутбук", "Сканер", "Прочее")
FIELDS = ("inv_number", "type", "name", "room", "status", "date_added", "responsible")


def normalize_item(item):
    return {field: str(item.get(field) or "").strip() for field in FIELDS}


def format_item(item):
    item = normalize_item(item)
    return (
        f"{item['inv_number']} | {item['type']} | {item['name']} | "
        f"каб. {item['room']} | {item['status']}"
    )


def next_number(items):
    max_num = 0
    for item in items:
        number = normalize_item(item)["inv_number"]
        if number.startswith("INV-"):
            try:
                max_num = max(max_num, int(number.split("-")[1]))
            except ValueError:
                pass
    return f"INV-{max_num + 1:04d}"


def check_item(data, items):
    inv_number = data["inv_number"].strip()
    item_type = data["type"].strip()
    name = data["name"].strip()
    room = data["room"].strip()
    status = data["status"].strip()

    if not inv_number:
        return "Поле «номер» пустое."
    if not inv_number.startswith("INV-") or not inv_number[4:].isdigit():
        return "Номер должен быть в формате INV-0001 (буквы INV-, затем цифры)."

    if not item_type:
        return "Поле «тип» пустое."
    if item_type not in TYPES:
        return f"Тип должен быть одним из: {', '.join(TYPES)}."

    if not name:
        return "Поле «наименование» пустое."
    if not any(c.isalpha() for c in name):
        return "Наименование должно содержать хотя бы одну букву."

    if not room:
        return "Поле «кабинет» пустое."
    if not room.isdigit():
        return "Кабинет должен состоять только из цифр."

    if status not in STATUSES:
        return "Состояние: исправно / требует ремонта / списано."

    for item in items:
        if item["inv_number"] == inv_number:
            return f"Номер {inv_number} уже есть."

    return None


def add_item(items, data):
    error = check_item(data, items)
    if error:
        return error
    items.append(data)
    return None


def find_by_number(items, number):
    for item in items:
        if item["inv_number"] == number:
            return item
    return None


def find_by_room(items, room):
    return [item for item in items if item["room"] == room]


def update_item(items, number, room=None, status=None):
    item = find_by_number(items, number)
    if item is None:
        return "Запись не найдена."
    if status is not None and status not in STATUSES:
        return "Состояние: исправно / требует ремонта / списано."
    if room:
        if not room.isdigit():
            return "Кабинет должен состоять только из цифр."
        item["room"] = room
    if status:
        item["status"] = status
    return None


def delete_item(items, number):
    item = find_by_number(items, number)
    if item is None:
        return "Запись не найдена."
    items.remove(item)
    return None
