"""Order-preserving collection operations with explicit input contracts."""

import re
from collections import Counter
from collections.abc import Hashable, Iterable

_WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")


def ordered_unique[T: Hashable](items: Iterable[T]) -> list[T]:
    """Keep the first occurrence of each hashable value, preserving input order.

    Consume the iterable once without mutating it. Python hashing/equality rules
    apply (for example, 1 and True compare equal). Unhashable values raise
    TypeError. Expected O(n) time and O(k) space for k distinct values, assuming
    constant-time hashing and equality.
    """
    seen: set[T] = set()
    result: list[T] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def word_frequencies(text: str, *, case_sensitive: bool = False) -> dict[str, int]:
    """Count Unicode letter words in order of first appearance.

    Punctuation, digits, underscores and hyphens separate words. Internal straight
    or curly apostrophes are retained, so contractions remain single words.
    Case-insensitive counting uses casefold; pass case_sensitive=True to opt out.
    Non-string text or a non-bool option raises TypeError. No Unicode normalization
    is performed: decomposed combining marks may split words. This is an exercise,
    not a natural-language tokenizer.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(case_sensitive, bool):
        raise TypeError("case_sensitive must be a bool")
    words = _WORD_PATTERN.finditer(text)
    return dict(
        Counter(
            match.group() if case_sensitive else match.group().casefold()
            for match in words
        )
    )
