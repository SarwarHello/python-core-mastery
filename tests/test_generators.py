"""Laziness, one-pass consumption, bounds and error propagation."""

from itertools import count, islice

import pytest

from core_mastery.generators import batches, running_totals


@pytest.mark.parametrize(
    ("values", "size", "expected"),
    [
        ([], 2, []),
        ([1], 2, [(1,)]),
        ([1, 2, 3, 4], 2, [(1, 2), (3, 4)]),
        ([1, 2, 3], 2, [(1, 2), (3,)]),
        ([1, 2], 1, [(1,), (2,)]),
        (["a", None, "b"], 9, [("a", None, "b")]),
    ],
)
def test_batch_contents(values, size, expected):
    original = values.copy()
    assert list(batches(values, size)) == expected
    assert values == original


@pytest.mark.parametrize(
    "size,error",
    [
        (0, ValueError),
        (-1, ValueError),
        (True, TypeError),
        (1.5, TypeError),
        ("2", TypeError),
    ],
)
def test_invalid_size_is_rejected_before_iteration(size, error):
    class Forbidden:
        def __iter__(self):
            raise AssertionError("input must not be acquired")

    with pytest.raises(error):
        batches(Forbidden(), size)


def test_batches_are_lazy_and_do_not_read_ahead():
    visited = []

    def source():
        for value in range(5):
            visited.append(value)
            yield value

    result = batches(source(), 2)
    assert visited == []
    assert next(result) == (0, 1)
    assert visited == [0, 1]
    assert list(result) == [(2, 3), (4,)]
    assert list(result) == []


def test_batch_input_iterator_acquired_only_once_and_lazily():
    class Once:
        def __init__(self):
            self.calls = 0

        def __iter__(self):
            self.calls += 1
            assert self.calls == 1
            return iter([1, 2, 3])

    source = Once()
    result = batches(source, 2)
    assert source.calls == 0
    assert list(result) == [(1, 2), (3,)]
    assert source.calls == 1


def test_infinite_source_can_be_consumed_in_finite_batches():
    assert list(islice(batches(count(), 2), 3)) == [(0, 1), (2, 3), (4, 5)]


def test_partial_batch_is_not_yielded_after_input_error():
    error = RuntimeError("source failed")

    def source():
        yield 1
        raise error

    with pytest.raises(RuntimeError) as caught:
        next(batches(source(), 2))
    assert caught.value is error


def test_batch_close_does_not_close_caller_owned_source():
    source = iter([1, 2, 3])
    result = batches(source, 1)
    assert next(result) == (1,)
    result.close()
    assert next(source) == 2


@pytest.mark.parametrize(
    "values,start,expected",
    [
        ([], 10, []),
        ([1, 2, 3], 0, [1, 3, 6]),
        ([2, -5, 0], 10, [12, 7, 7]),
        ([0], 0, [0]),
    ],
)
def test_running_totals(values, start, expected):
    original = values.copy()
    assert list(running_totals(iter(values), start=start)) == expected
    assert values == original


def test_running_totals_is_lazy_and_one_shot():
    visited = []

    def source():
        for value in [2, 3]:
            visited.append(value)
            yield value

    result = running_totals(source())
    assert visited == []
    assert next(result) == 2
    assert visited == [2]
    assert list(result) == [5]
    assert list(result) == []


def test_running_totals_propagates_input_failure():
    def source():
        yield 1
        raise ValueError("broken input")

    result = running_totals(source())
    assert next(result) == 1
    with pytest.raises(ValueError, match="broken input"):
        next(result)


def test_generator_pipeline():
    assert list(batches(running_totals([2, 3, 4, 1]), 3)) == [(2, 5, 9), (10,)]
