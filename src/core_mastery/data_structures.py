"""Focused exercises for lists, tuples, sets and dictionaries."""

from collections.abc import Iterable


def top_scores(scores: list[int], limit: int = 3) -> list[int]:
    """Return a descending copy of up to limit scores, retaining duplicates.

    Scores follow the annotated integer contract. Negative limits are rejected.
    """
    if type(limit) is not int:
        raise TypeError("limit must be an integer")
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    return sorted(scores, reverse=True)[:limit]


def score_bounds(scores: Iterable[int]) -> tuple[int, int]:
    """Return (minimum, maximum) in one pass; reject an empty iterable."""
    iterator = iter(scores)
    try:
        low = high = next(iterator)
    except StopIteration:
        raise ValueError("scores must not be empty") from None
    for score in iterator:
        low = min(low, score)
        high = max(high, score)
    return low, high


def compare_skills(
    required: set[str], available: set[str]
) -> tuple[set[str], set[str]]:
    """Return fresh (matched, missing) sets with case-sensitive membership."""
    return required & available, required - available


def group_members(records: Iterable[tuple[str, str]]) -> dict[str, list[str]]:
    """Group (department, name) records in encounter order, keeping duplicates.

    Inputs must follow the annotated two-string tuple contract. Return a fresh
    list per department; no caller-owned collection is mutated.
    """
    groups: dict[str, list[str]] = {}
    for department, name in records:
        groups.setdefault(department, []).append(name)
    return groups
