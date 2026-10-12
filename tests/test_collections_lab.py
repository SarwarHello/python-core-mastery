"""Behavioural tests for the documented public collection contracts."""

import pytest

from core_mastery import ordered_unique, word_frequencies


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([], []),
        ([3, 1, 3, 2, 1], [3, 1, 2]),
        (["a", "a", "b"], ["a", "b"]),
        ([(1, 2), (1, 2), (2, 1)], [(1, 2), (2, 1)]),
        ([None, None, "a"], [None, "a"]),
        ([1, True, 0, False], [1, 0]),
    ],
)
def test_ordered_unique_contract(items, expected):
    original = items.copy()
    assert ordered_unique(items) == expected
    assert items == original


def test_ordered_unique_consumes_generator_once():
    visited = []

    def values():
        for value in [2, 1, 2]:
            visited.append(value)
            yield value

    stream = values()
    assert ordered_unique(stream) == [2, 1]
    assert visited == [2, 1, 2]
    assert list(stream) == []


def test_ordered_unique_rejects_unhashable_values():
    with pytest.raises(TypeError):
        ordered_unique([[1], [1]])


def test_ordered_unique_handles_hash_collisions():
    class CollidingValue:
        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return 0

        def __eq__(self, other):
            if not isinstance(other, CollidingValue):
                return NotImplemented
            return self.value == other.value

    first = CollidingValue("first")
    second = CollidingValue("second")
    result = ordered_unique([first, second, CollidingValue("first")])
    assert result == [first, second]
    assert result[0] is first


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", {}),
        (" \t\n", {}),
        ("123 _ -- !!!", {}),
        ("Python, python! SQL and Python.", {"python": 3, "sql": 1, "and": 1}),
        ("red\nblue\tred", {"red": 2, "blue": 1}),
        ("don't DON'T don’t", {"don't": 2, "don’t": 1}),
        ("Café CAFÉ Straße STRASSE", {"café": 2, "strasse": 2}),
        ("end-to_end42end", {"end": 3, "to": 1}),
        ("'quoted'", {"quoted": 1}),
        ("cafe\u0301 café", {"cafe": 1, "café": 1}),
    ],
)
def test_word_frequencies_contract(text, expected):
    assert word_frequencies(text) == expected


def test_word_frequencies_can_preserve_case():
    assert word_frequencies("Python python Python", case_sensitive=True) == {
        "Python": 2,
        "python": 1,
    }


def test_word_frequencies_preserves_first_appearance_order():
    assert list(word_frequencies("Zebra apple APPLE banana zebra")) == [
        "zebra",
        "apple",
        "banana",
    ]


@pytest.mark.parametrize("text", [None, 123, b"Python", ["Python"]])
def test_word_frequencies_rejects_non_string_input(text):
    with pytest.raises(TypeError, match="text must be a string"):
        word_frequencies(text)


@pytest.mark.parametrize("option", [None, 1, "false"])
def test_word_frequencies_rejects_non_bool_option(option):
    with pytest.raises(TypeError, match="case_sensitive must be a bool"):
        word_frequencies("Python", case_sensitive=option)
