# Day 4 — OOP, inheritance and encapsulation

[Implementation](../src/core_mastery/oop_lab.py) · [Tests](../tests/test_oop_lab.py)

```powershell
.venv\Scripts\python.exe 04_oop/examples.py
```

Expected output:

```text
PEN: 4
BOX: 3
Total: 7
restock exceeds capacity
After withdrawal: 6
```

## Classes and contracts

- **StockItem:** constructor validates a nonblank SKU and nonnegative integer
  quantity. Read-only properties expose state; restock/withdraw enforce positive
  integer changes and prevent negative stock. Bool is explicitly rejected.
- **LimitedStockItem:** inherits StockItem, calls super() during initialization,
  overrides restock to enforce capacity, and inherits withdraw unchanged. A shared
  list[StockItem] interface demonstrates polymorphism. The base restock contract
  explicitly permits storage-policy rejection, so callers must handle ValueError.
- **Inventory:** composes stock items rather than inheriting from one. It owns
  membership, rejects duplicate case-sensitive SKUs and calculates live totals.
  Each inventory has its own dictionary; each stock item has its own quantity.

Encapsulation means maintaining invariants through a documented interface.
Underscored fields signal implementation details; Python does not make them a
security boundary. Read-only properties block ordinary assignment, not deliberate
modification of internal attributes. Tests exercise public behaviour rather than
reaching into internal state. Failed operations leave state unchanged.

The tuple returned by items is a membership snapshot, not a deep copy: its stock
objects are shared, and changing their quantities updates live inventory totals.
This is intentional and tested. SKU should not change after registration.

Inheritance fits an **is-a** relationship with a compatible contract. Composition
fits a **has-a** relationship: an inventory contains stock items. For many
independent capacity/pricing/storage policies, composing policy objects may scale
better than adding a subclass for every combination. This exercise keeps one
small hierarchy to make super(), overriding and inherited methods explicit.

## Complexity and limitations

Quantity operations use a fixed number of integer operations (large-integer cost
still depends on operand size). Adding a SKU is expected O(1), while items and
total_quantity are O(n); a membership snapshot allocates O(n) references.
This is an in-memory learning model, with no database, concurrent-update safety,
reservation system, audit history or production inventory guarantees.

Tests cover constructor validation, read-only properties, independent instances,
failed-state preservation, exact-capacity boundaries, inherited behaviour,
polymorphic calls, duplicate membership and shared-reference semantics.

Review: explain class versus instance, self, super(), method overriding, why
properties help preserve invariants, and why Inventory does not inherit StockItem.
