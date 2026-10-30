"""Inventory examples for encapsulation, inheritance and composition."""


def _integer(value: int, name: str, *, minimum: int = 0) -> None:
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")


class StockItem:
    """A stock identity with read-only properties and validated quantity changes.

    Underscored attributes are implementation details, not a security boundary.
    Failed public operations leave the quantity unchanged.
    """

    def __init__(self, sku: str, quantity: int = 0) -> None:
        if not isinstance(sku, str):
            raise TypeError("sku must be a string")
        if not sku.strip():
            raise ValueError("sku must not be blank")
        _integer(quantity, "quantity")
        self._sku = sku.strip()
        self._quantity = quantity

    @property
    def sku(self) -> str:
        """Return the case-sensitive, trimmed identifier."""
        return self._sku

    @property
    def quantity(self) -> int:
        """Return current stock; change it through restock or withdraw."""
        return self._quantity

    def restock(self, amount: int) -> None:
        """Add a positive integer amount, subject to the item's storage policy.

        Subclasses may impose a capacity and reject additions that exceed it.
        """
        _integer(amount, "amount", minimum=1)
        self._quantity += amount

    def withdraw(self, amount: int) -> None:
        """Remove a positive integer amount without allowing negative stock."""
        _integer(amount, "amount", minimum=1)
        if amount > self._quantity:
            raise ValueError("insufficient stock")
        self._quantity -= amount


class LimitedStockItem(StockItem):
    """Stock constrained by a fixed capacity; inherits withdrawal behaviour."""

    def __init__(self, sku: str, capacity: int, quantity: int = 0) -> None:
        _integer(capacity, "capacity")
        super().__init__(sku, quantity)
        if quantity > capacity:
            raise ValueError("quantity exceeds capacity")
        self._capacity = capacity

    @property
    def capacity(self) -> int:
        """Return the item's maximum quantity."""
        return self._capacity

    def restock(self, amount: int) -> None:
        """Reject an addition above capacity before changing state."""
        _integer(amount, "amount", minimum=1)
        if self.quantity + amount > self.capacity:
            raise ValueError("restock exceeds capacity")
        super().restock(amount)


class Inventory:
    """Compose stock items in insertion order, with unique case-sensitive SKUs.

    Membership snapshots are tuples, but their items remain the original mutable
    objects. External restock/withdraw operations are reflected in totals.
    """

    def __init__(self) -> None:
        self._items: dict[str, StockItem] = {}

    def add(self, item: StockItem) -> None:
        """Register a stock item or subclass; reject duplicate SKU membership."""
        if not isinstance(item, StockItem):
            raise TypeError("item must be a StockItem")
        if item.sku in self._items:
            raise ValueError(f"duplicate sku: {item.sku}")
        self._items[item.sku] = item

    @property
    def items(self) -> tuple[StockItem, ...]:
        """Return a membership snapshot, not a deep copy of each stock item."""
        return tuple(self._items.values())

    @property
    def total_quantity(self) -> int:
        """Sum live stock quantities across registered items."""
        return sum(item.quantity for item in self._items.values())
