"""Function contracts, validation and callable semantics."""

import pytest

from core_mastery.functions_lab import calculate_total, transform_values


@pytest.mark.parametrize(
    ("price", "quantity", "discount", "expected"),
    [
        (250, 3, 10, 675),
        (101, 1, 10, 90),
        (250, 0, 0, 0),
        (0, 5, 0, 0),
        (250, 2, 100, 0),
    ],
)
def test_calculate_total(price, quantity, discount, expected):
    assert calculate_total(price, quantity, discount_percent=discount) == expected


def test_default_quantity_and_discount():
    assert calculate_total(250) == 250


@pytest.mark.parametrize(
    "kwargs",
    [
        {"unit_price": -1},
        {"unit_price": 1, "quantity": -1},
        {"unit_price": 1, "discount_percent": -1},
        {"unit_price": 1, "discount_percent": 101},
    ],
)
def test_invalid_ranges(kwargs):
    with pytest.raises(ValueError):
        calculate_total(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"unit_price": True},
        {"unit_price": 1.5},
        {"unit_price": 1, "quantity": "2"},
        {"unit_price": 1, "discount_percent": False},
    ],
)
def test_invalid_types(kwargs):
    with pytest.raises(TypeError):
        calculate_total(**kwargs)


def test_discount_is_keyword_only():
    with pytest.raises(TypeError):
        calculate_total(250, 3, 10)


def test_transform_generator_order_and_call_count():
    calls = []

    def stringify(value):
        calls.append(value)
        return str(value)

    assert transform_values(iter([3, 1, 3]), stringify) == ["3", "1", "3"]
    assert calls == [3, 1, 3]


def test_transform_does_not_mutate_input():
    values = [1, 2]
    assert transform_values(values, lambda n: n * 2) == [2, 4]
    assert values == [1, 2]


def test_empty_transform_does_not_call_callback():
    def forbidden(value):
        raise AssertionError("callback must not run")

    assert transform_values([], forbidden) == []


def test_transform_propagates_callback_error():
    with pytest.raises(ZeroDivisionError):
        transform_values([2, 0], lambda n: 1 / n)
