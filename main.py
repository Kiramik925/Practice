from inventory import format_item
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


def show_items():
    items = load_items()
    if not items:
        print("Записей пока нет.")
        return
    print("\nОборудование (демонстрационные данные):")
    for item in items:
        print("  " + format_item(item))
    print(f"\nВсего записей: {len(items)}")


def main():
    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            show_items()
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Этот пункт появится в следующих спринтах.")


if __name__ == "__main__":
    main()
