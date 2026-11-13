from inventory import (
    STATUSES,
    add_item,
    delete_item,
    filter_items,
    find_by_number,
    format_item,
    next_number,
    update_item,
)
from storage import last_message, load_items, save_items

MENU = """
=== Учёт инвентаря ===
1. Показать оборудование
2. Добавить оборудование
3. Найти оборудование
4. Изменить оборудование
5. Удалить оборудование
6. Отбор по кабинету и состоянию
0. Выход
"""

STATUS_CHOICES = {"1": STATUSES[0], "2": STATUSES[1], "3": STATUSES[2]}


def ask(prompt):
    return input(prompt).strip()


def load():
    items = load_items()
    problem = last_message()
    if problem:
        print("\n" + problem)
    return items


def print_items(items):
    for item in items:
        print("  " + format_item(item))
    print(f"\nВсего: {len(items)}")


def save_change(items, message):
    error = save_items(items)
    if error:
        print("\nОшибка:", error)
        return
    print("\n" + message)


def require_item(items, number):
    item = find_by_number(items, number)
    if item is None:
        print("Запись не найдена.")
    return item


def show_items():
    items = load()
    if not items:
        print("Записей нет.")
        return
    print("\nОборудование:")
    print_items(items)


def add_new_item():
    items = load()
    default = next_number(items)
    number = ask(f"Номер [{default}]: ") or default
    data = {
        "inv_number": number,
        "type": ask("Тип: "),
        "name": ask("Наименование: "),
        "room": ask("Кабинет: "),
        "status": ask("Состояние (исправно/требует ремонта/списано): "),
        "date_added": ask("Дата поступления: "),
        "responsible": ask("Ответственный: "),
    }
    error = add_item(items, data)
    if error:
        print("\nОшибка:", error)
        return
    save_change(items, f"Запись {number.upper()} добавлена.")


def search_item():
    items = load()
    print("\nПоиск: 1 — по номеру, 2 — по кабинету")
    mode = ask("Выбор: ")

    if mode == "1":
        number = ask("Номер: ")
        if not number:
            print("Номер не введён.")
            return
        item = find_by_number(items, number)
        if item is None:
            print("Не найдено.")
            return
        print(format_item(item))
    elif mode == "2":
        room = ask("Кабинет: ")
        found = filter_items(items, room=room)
        if not found:
            print("Не найдено.")
            return
        print_items(found)
    else:
        print("Неверный выбор.")


def filter_by_params():
    items = load()
    room = ask("Кабинет (Enter — любой): ")
    print("Состояние: 1 — исправно, 2 — требует ремонта, 3 — списано, Enter — любое")
    choice = ask("Выбор: ")

    if choice and choice not in STATUS_CHOICES:
        print("Неверный выбор.")
        return

    status = STATUS_CHOICES.get(choice)
    if not room and not status:
        print("Не задан ни один признак отбора.")
        return

    found = filter_items(items, room=room or None, status=status)
    if not found:
        print("\nНичего не найдено.")
        return

    print("\nНайдено:")
    print_items(found)


def edit_item():
    items = load()
    number = ask("Номер записи: ")
    if require_item(items, number) is None:
        return

    room = ask("Новый кабинет (Enter — не менять): ")
    status = ask("Новое состояние (Enter — не менять): ")
    error = update_item(items, number, room or None, status or None)
    if error:
        print("\nОшибка:", error)
        return
    save_change(items, "Запись обновлена.")


def remove_item():
    items = load()
    number = ask("Номер записи для удаления: ")
    if require_item(items, number) is None:
        return

    if ask(f"Удалить {number}? (да/нет): ").lower() != "да":
        print("Удаление отменено.")
        return

    error = delete_item(items, number)
    if error:
        print("\nОшибка:", error)
        return
    save_change(items, "Запись удалена.")


ACTIONS = {
    "1": show_items,
    "2": add_new_item,
    "3": search_item,
    "4": edit_item,
    "5": remove_item,
    "6": filter_by_params,
}


def main():
    while True:
        print(MENU)
        choice = ask("Выберите пункт: ")

        if choice == "0":
            print("Выход.")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Неверный пункт.")
            continue

        action()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход.")
