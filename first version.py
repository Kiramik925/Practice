from inventory import InventoryItem, format_item
from storage import load_items

MENU = """
=== Система учёта инвентаря компьютерных классов ===
1. Показать оборудование
2. Добавить оборудование
3. Найти оборудование
4. Изменить оборудование
5. Удалить оборудование
0. Выход
"""


def show_items() -> None:
    records = load_items()
    if not records:
        print("Записей пока нет.")
        return
    print("\nОборудование (демонстрационные данные):")
    for data in records:
        print("  " + format_item(InventoryItem.from_dict(data)))
    print(f"\nВсего записей: {len(records)}")


def main() -> None:
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            show_items()
        elif choice == "2":
            print("Добавление будет реализовано в Спринте 2.")
        elif choice == "3":
            print("Поиск будет реализован в Спринте 3.")
        elif choice == "4":
            print("Изменение будет реализовано в Спринте 3.")
        elif choice == "5":
            print("Удаление будет реализовано в Спринте 3.")
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный пункт меню, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
