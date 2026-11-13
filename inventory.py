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
        number = normalize_item(item)["inv_number"].upper()
        if number.startswith("INV-") and number[4:].isdigit():
            max_num = max(max_num, int(number[4:]))
    return f"INV-{max_num + 1:04d}"


def validate_number(number):
    if not number:
        return "Поле «номер» пустое."
    if not number.upper().startswith("INV-") or not number[4:].isdigit():
        return "Номер должен быть в формате INV-0001 (буквы INV-, затем цифры)."
    return None


def validate_type(item_type):
    if not item_type:
        return "Поле «тип» пустое."
    if item_type not in TYPES:
        return f"Тип должен быть одним из: {', '.join(TYPES)}."
    return None


def validate_name(name):
    if not name:
        return "Поле «наименование» пустое."
    if not any(letter.isalpha() for letter in name):
        return "Наименование должно содержать хотя бы одну букву."
    return None


def validate_room(room):
    if not room:
        return "Поле «кабинет» пустое."
    if not room.isdigit():
        return "Кабинет должен состоять только из цифр."
    return None


def validate_status(status):
    if status not in STATUSES:
        return "Состояние: исправно / требует ремонта / списано."
    return None


def validate_item(data, items):
    clean = normalize_item(data)
    checks = (
        (validate_number, clean["inv_number"]),
        (validate_type, clean["type"]),
        (validate_name, clean["name"]),
        (validate_room, clean["room"]),
        (validate_status, clean["status"]),
    )
    for check, value in checks:
        error = check(value)
        if error:
            return error
    if find_by_number(items, clean["inv_number"]):
        return f"Номер {clean['inv_number'].upper()} уже есть."
    return None


def add_item(items, data):
    error = validate_item(data, items)
    if error:
        return error
    clean = normalize_item(data)
    clean["inv_number"] = clean["inv_number"].upper()
    items.append(clean)
    return None


def find_by_number(items, number):
    wanted = normalize_item({"inv_number": number})["inv_number"].upper()
    if not wanted:
        return None
    for item in items:
        if normalize_item(item)["inv_number"].upper() == wanted:
            return item
    return None


def filter_items(items, room=None, status=None):
    room = (room or "").strip()
    result = []
    for item in items:
        clean = normalize_item(item)
        if room and clean["room"] != room:
            continue
        if status and clean["status"] != status:
            continue
        result.append(item)
    return result


def update_item(items, number, room=None, status=None):
    item = find_by_number(items, number)
    if item is None:
        return "Запись не найдена."
    if room:
        error = validate_room(room)
        if error:
            return error
    if status:
        error = validate_status(status)
        if error:
            return error
    if room:
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
