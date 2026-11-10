STATUSES = ("исправно", "требует ремонта", "списано")


def format_item(item):
    return (
        f"{item['inv_number']} | {item['type']} | {item['name']} | "
        f"каб. {item['room']} | {item['status']}"
    )


def next_number(items):
    max_num = 0
    for item in items:
        number = item.get("inv_number", "")
        if number.startswith("INV-"):
            try:
                max_num = max(max_num, int(number.split("-")[1]))
            except ValueError:
                pass
    return f"INV-{max_num + 1:04d}"


def check_item(data, items):
    for field, label in (
        ("inv_number", "номер"),
        ("type", "тип"),
        ("name", "наименование"),
        ("room", "кабинет"),
        ("status", "состояние"),
    ):
        if not data[field].strip():
            return f"Поле «{label}» пустое."

    if data["status"] not in STATUSES:
        return "Состояние: исправно / требует ремонта / списано."

    for item in items:
        if item["inv_number"] == data["inv_number"]:
            return f"Номер {data['inv_number']} уже есть."

    return None


def add_item(items, data):
    error = check_item(data, items)
    if error:
        return error
    items.append(data)
    return None