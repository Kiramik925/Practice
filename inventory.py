"""Операции с инвентарными записями (Спринт 1 — каркас)."""


def format_item(item):
    """Возвращает строку для вывода одной записи в списке."""
    return (
        f"{item['inv_number']} | {item['type']} | {item['name']} | "
        f"каб. {item['room']} | {item['status']}"
    )
