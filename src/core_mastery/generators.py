"""Lazy, one-pass iteration with explicit buffering behaviour."""

from collections.abc import Iterable, Iterator
from itertools import islice


def batches[T](values: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Return a lazy iterator of tuples, retaining a partial final batch.

    Validate size immediately, before acquiring or consuming the input iterator.
    Each next() consumes at most size values. Memory is O(size), excluding input
    and output retained by the caller. Errors from the input propagate. Input
    ownership stays with the caller; closing this wrapper does not close input.
    """
    if type(size) is not int:
        raise TypeError("size must be an integer")
    if size < 1:
        raise ValueError("size must be positive")

    def generate() -> Iterator[tuple[T, ...]]:
        iterator = iter(values)
        while batch := tuple(islice(iterator, size)):
            yield batch

    return generate()


def running_totals(values: Iterable[int], *, start: int = 0) -> Iterator[int]:
    """Yield each cumulative total, without yielding the initial start itself.

    Follow the annotated integer contract. Input is acquired and consumed only
    on iteration. O(n) additions and O(1) extra state (integer sizes may grow).
    Empty input yields nothing. Input errors propagate unchanged.
    """
    total = start
    for value in values:
        total += value
        yield total
