"""Functions, parameters, return types and higher-order functions."""

from collections.abc import Callable, Iterable


def calculate_total(
    unit_price: int, quantity: int = 1, *, discount_percent: int = 0
) -> int:
    """Return an integer-pence total, rounded down after a percentage discount.

    Price and quantity must be nonnegative integers; discount is an integer in
    [0, 100]. Booleans are rejected even though bool subclasses int.
    """
    for name, value in (
        ("unit_price", unit_price),
        ("quantity", quantity),
        ("discount_percent", discount_percent),
    ):
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        if value < 0:
            raise ValueError(f"{name} must be nonnegative")
    if discount_percent > 100:
        raise ValueError("discount_percent must not exceed 100")
    return unit_price * quantity * (100 - discount_percent) // 100


def transform_values[T, U](values: Iterable[T], operation: Callable[[T], U]) -> list[U]:
    """Apply an operation once per value, retaining order and propagating errors.

    The input iterable is not mutated by this function. A supplied callback may
    have its own side effects; this function does not copy mutable input values.
    """
    return [operation(value) for value in values]
