"""Observable contracts for all four collection types."""

import pytest

from core_mastery.data_structures import (
    compare_skills,
    group_members,
    score_bounds,
    top_scores,
)


@pytest.mark.parametrize(
    ("scores", "limit", "expected"),
    [
        ([], 3, []),
        ([7, 9, 7, 2], 2, [9, 7]),
        ([4, 4, 1], 9, [4, 4, 1]),
        ([1, 2], 0, []),
        ([-5, -1], 1, [-1]),
    ],
)
def test_top_scores(scores, limit, expected):
    original = scores.copy()
    result = top_scores(scores, limit)
    assert result == expected
    assert scores == original
    assert result is not scores


def test_top_scores_rejects_negative_limit():
    with pytest.raises(ValueError):
        top_scores([1], -1)


@pytest.mark.parametrize("limit", [True, 1.5])
def test_top_scores_rejects_invalid_limit(limit):
    with pytest.raises(TypeError):
        top_scores([1], limit)


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([7, 9, 2], (2, 9)),
        ([4], (4, 4)),
        ([-3, -8], (-8, -3)),
    ],
)
def test_score_bounds(scores, expected):
    result = score_bounds(iter(scores))
    assert isinstance(result, tuple)
    low, high = result
    assert (low, high) == expected


def test_empty_bounds():
    with pytest.raises(ValueError, match="must not be empty"):
        score_bounds(iter([]))


@pytest.mark.parametrize(
    ("required", "available", "expected"),
    [
        ({"Python", "SQL"}, {"Python", "Git"}, ({"Python"}, {"SQL"})),
        (set(), {"Python"}, (set(), set())),
        ({"Python"}, set(), (set(), {"Python"})),
        ({"Python"}, {"python"}, (set(), {"Python"})),
    ],
)
def test_compare_skills(required, available, expected):
    before = (required.copy(), available.copy())
    matched, missing = compare_skills(required, available)
    assert (matched, missing) == expected
    matched.add("new")
    missing.add("new")
    assert (required, available) == before


def test_group_members_order_duplicates_and_independent_lists():
    records = [("backend", "Ada"), ("data", "Lin"), ("backend", "Ada")]
    original = records.copy()
    groups = group_members(iter(records))
    assert list(groups) == ["backend", "data"]
    assert groups == {"backend": ["Ada", "Ada"], "data": ["Lin"]}
    groups["backend"].append("Sam")
    assert groups["data"] == ["Lin"]
    assert records == original
    assert group_members(records)["backend"] == ["Ada", "Ada"]


def test_empty_groups():
    assert group_members([]) == {}
