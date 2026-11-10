from inventory import format_item, next_number, add_item
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


def main():
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            show_items()
        elif choice == "2":
            add_new_item()
        elif choice == "3":
            print("Поиск — в Спринте 3.")
        elif choice == "4":
            print("Изменение — в Спринте 3.")
        elif choice == "5":
            print("Удаление — в Спринте 3.")
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный пункт.")


if __name__ == "__main__":
    main()