"""Public state, validation, inheritance and composition contracts."""

import pytest

from core_mastery.oop_lab import Inventory, LimitedStockItem, StockItem


def test_identity_and_default_state():
    item = StockItem(" PEN ")
    assert (item.sku, item.quantity) == ("PEN", 0)


@pytest.mark.parametrize("sku", ["", " ", "\t\n"])
def test_blank_sku(sku):
    with pytest.raises(ValueError):
        StockItem(sku)


@pytest.mark.parametrize("sku", [None, 3])
def test_wrong_sku_type(sku):
    with pytest.raises(TypeError):
        StockItem(sku)


@pytest.mark.parametrize("quantity", [True, 1.5, "2"])
def test_wrong_quantity_type(quantity):
    with pytest.raises(TypeError):
        StockItem("PEN", quantity)


def test_negative_initial_stock():
    with pytest.raises(ValueError):
        StockItem("PEN", -1)


@pytest.mark.parametrize("attribute", ["sku", "quantity"])
def test_public_properties_are_read_only(attribute):
    item = StockItem("PEN", 2)
    with pytest.raises(AttributeError):
        setattr(item, attribute, 10)
    assert (item.sku, item.quantity) == ("PEN", 2)


def test_instances_have_independent_state():
    first, second = StockItem("PEN"), StockItem("PEN")
    first.restock(3)
    assert second.quantity == 0
    first.withdraw(3)
    assert first.quantity == 0


@pytest.mark.parametrize("method", ["restock", "withdraw"])
@pytest.mark.parametrize(
    "amount,error",
    [(0, ValueError), (-1, ValueError), (True, TypeError), (1.5, TypeError)],
)
def test_invalid_mutation_preserves_state(method, amount, error):
    item = StockItem("PEN", 3)
    with pytest.raises(error):
        getattr(item, method)(amount)
    assert item.quantity == 3


def test_insufficient_stock_preserves_state():
    item = StockItem("PEN", 3)
    with pytest.raises(ValueError, match="insufficient"):
        item.withdraw(4)
    assert item.quantity == 3


def test_limited_item_inherits_withdrawal_and_reuses_capacity():
    item = LimitedStockItem("BOX", 5, 2)
    assert isinstance(item, StockItem)
    item.restock(3)
    assert item.quantity == item.capacity == 5
    with pytest.raises(ValueError, match="capacity"):
        item.restock(1)
    assert item.quantity == 5
    item.withdraw(2)
    item.restock(2)
    assert item.quantity == 5


@pytest.mark.parametrize(
    "capacity,error", [(-1, ValueError), (True, TypeError), (1.5, TypeError)]
)
def test_invalid_capacity(capacity, error):
    with pytest.raises(error):
        LimitedStockItem("BOX", capacity)


def test_initial_quantity_over_capacity():
    with pytest.raises(ValueError, match="exceeds capacity"):
        LimitedStockItem("BOX", 2, 3)


def test_zero_capacity_is_valid_but_cannot_hold_stock():
    item = LimitedStockItem("BOX", 0)
    assert item.quantity == 0
    with pytest.raises(ValueError):
        item.restock(1)


def test_capacity_is_read_only():
    item = LimitedStockItem("BOX", 2)
    with pytest.raises(AttributeError):
        item.capacity = 3


@pytest.mark.parametrize("amount", [True, "1", 1.5])
def test_subclass_rejects_wrong_types_without_mutation(amount):
    item = LimitedStockItem("BOX", 3, 1)
    with pytest.raises(TypeError):
        item.restock(amount)
    assert item.quantity == 1


def test_polymorphic_restock():
    items: list[StockItem] = [StockItem("PEN"), LimitedStockItem("BOX", 2)]
    for item in items:
        item.restock(2)
    assert [item.quantity for item in items] == [2, 2]


def test_inventory_membership_and_live_totals():
    inventory = Inventory()
    first, second = StockItem("PEN", 2), LimitedStockItem("BOX", 5, 3)
    inventory.add(first)
    snapshot = inventory.items
    inventory.add(second)
    assert snapshot == (first,)
    assert inventory.items == (first, second)
    assert inventory.total_quantity == 5
    first.withdraw(1)
    assert inventory.total_quantity == 4
    assert inventory.items[0] is first


def test_empty_inventories_do_not_share_membership():
    first, second = Inventory(), Inventory()
    first.add(StockItem("PEN", 1))
    assert second.items == ()
    assert second.total_quantity == 0


def test_duplicate_sku_rejected_without_replacement():
    inventory = Inventory()
    item = StockItem("PEN", 2)
    inventory.add(item)
    with pytest.raises(ValueError, match="duplicate"):
        inventory.add(StockItem(" PEN ", 10))
    assert inventory.items == (item,)
    assert inventory.total_quantity == 2


def test_skus_are_case_sensitive():
    inventory = Inventory()
    inventory.add(StockItem("PEN"))
    inventory.add(StockItem("pen"))
    assert len(inventory.items) == 2


def test_inventory_rejects_other_objects():
    inventory = Inventory()
    with pytest.raises(TypeError):
        inventory.add("PEN")
    assert inventory.items == ()
