"""Run from the repository root after installing the package."""

from core_mastery.oop_lab import Inventory, LimitedStockItem, StockItem


def main() -> None:
    """Show a shared interface, an overridden policy and composed objects."""
    items: list[StockItem] = [StockItem("PEN", 2), LimitedStockItem("BOX", 5, 1)]
    inventory = Inventory()
    for item in items:
        item.restock(2)
        inventory.add(item)
        print(f"{item.sku}: {item.quantity}")
    print(f"Total: {inventory.total_quantity}")
    try:
        items[1].restock(3)
    except ValueError as error:
        print(error)
    items[1].withdraw(1)
    print(f"After withdrawal: {inventory.total_quantity}")


if __name__ == "__main__":
    main()
