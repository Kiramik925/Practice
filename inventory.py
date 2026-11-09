
def format_item(item):
    return (
        f"{item['inv_number']} | {item['type']} | {item['name']} | "
        f"каб. {item['room']} | {item['status']}"
    )
