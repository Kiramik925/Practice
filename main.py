from inventory import (
    format_item,
    next_number,
    add_item,
    find_by_number,
    find_by_room,
    update_item,
    delete_item,
)
from storage import load_items, save_items

MENU = """
=== Учёт инвентаря ===
1. Показать оборудование
2. Добавить оборудование
3. Найти оборудование
4. Изменить оборудование
5. Удалить оборудование
0. Выход
"""


def show_items():
    items = load_items()
    if not items:
        print("Записей нет.")
        return
    print("\nОборудование:")
    for item in items:
        print("  " + format_item(item))
    print(f"\nВсего: {len(items)}")


def add_new_item():
    items = load_items()

    inv_number = input(f"Номер [{next_number(items)}]: ").strip() or next_number(items)
    data = {
        "inv_number": inv_number,
        "type": input("Тип: ").strip(),
        "name": input("Наименование: ").strip(),
        "room": input("Кабинет: ").strip(),
        "status": input("Состояние (исправно/требует ремонта/списано): ").strip(),
        "date_added": input("Дата поступления: ").strip(),
        "responsible": input("Ответственный: ").strip(),
    }

    error = add_item(items, data)
    if error:
        print("\nОшибка:", error)
        return

    save_items(items)
    print(f"\nЗапись {inv_number} добавлена.")


def search_item():
    items = load_items()
    print("\nПоиск: 1 — по номеру, 2 — по кабинету")
    mode = input("Выбор: ").strip()

    if mode == "1":
        number = input("Номер: ").strip()
        if not number:
            print("Номер не введён.")
            return
        item = find_by_number(items, number)
        if item is None:
            print("Не найдено.")
            return
        print(format_item(item))
    elif mode == "2":
        room = input("Кабинет: ").strip()
        found = find_by_room(items, room)
        if not found:
            print("Не найдено.")
            return
        for item in found:
            print(format_item(item))
    else:
        print("Неверный выбор.")


def edit_item():
    items = load_items()
    number = input("Номер записи: ").strip()
    if find_by_number(items, number) is None:
        print("Запись не найдена.")
        return

    room = input("Новый кабинет (Enter — не менять): ").strip()
    status = input("Новое состояние (Enter — не менять): ").strip()

    error = update_item(items, number, room or None, status or None)
    if error:
        print("\nОшибка:", error)
        return

    save_items(items)
    print("Запись обновлена.")


def remove_item():
    items = load_items()
    number = input("Номер записи для удаления: ").strip()
    if find_by_number(items, number) is None:
        print("Запись не найдена.")
        return

    confirm = input(f"Удалить {number}? (да/нет): ").strip().lower()
    if confirm != "да":
        print("Удаление отменено.")
        return

    error = delete_item(items, number)
    if error:
        print("\nОшибка:", error)
        return

    save_items(items)
    print("Запись удалена.")


def main():
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            show_items()
        elif choice == "2":
            add_new_item()
        elif choice == "3":
            search_item()
        elif choice == "4":
            edit_item()
        elif choice == "5":
            remove_item()
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный пункт.")


if __name__ == "__main__":
    main()