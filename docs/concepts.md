# Day 1: collections and contracts

## Ordered deduplication

A set gives expected constant-time membership checks but should not be used as
an ordering guarantee. Keep a separate result list and append only on first
encounter. A single loop accepts generators without consuming them in advance.
Python set equality deliberately treats `1` and `True` as equal. Hash collisions
do not mean equal values: sets still compare equality when hashes collide.

For n inputs and k distinct values, expected time is O(n), assuming constant-cost
hash/equality operations, with O(k) auxiliary and result space. Pathological hash
collisions can degrade performance. Lists and dictionaries are unhashable and
are outside this function's contract. `dict.fromkeys(items)` is a concise
alternative for this same contract; the explicit loop exposes the mechanics.

## Word counts

Tokenization defines what gets counted; Counter handles counting. `casefold()`
is stronger than `lower()` for caseless Unicode matching, including German sharp
s. Normalization happens on each matched word, and dictionaries preserve first
insertion order. The returned ordinary dictionary keeps the public result small
and familiar, without exposing Counter's missing-key behaviour.

The tokenizer matches Unicode letter runs with optional internal apostrophes.
Numbers/underscores/hyphens separate words. It is not a language model: scripts
without spaces, decomposed combining marks, and typographic variants need richer
rules in a real text-processing service. No Unicode normalization is performed.

For input length m, token scanning/counting takes expected O(m) time; stored keys
and counts use space proportional to the distinct word content. A match iterator
avoids retaining a list of every occurrence. The returned dictionary necessarily
stores the vocabulary.

## Interview practice

1. Why does a separate list preserve order while a set speeds up membership?
2. What changes if inputs contain mutable lists or expensive equality methods?
3. How does a generator differ from a reusable list?
4. Why can lowercasing miss matches that casefolding catches?
5. Which tests describe observable contracts instead of internal implementation?

## Tooling references

- [PyPA: pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [GitHub: Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)

The package uses a src layout so tests exercise an installed package, rather than
accidentally importing a top-level source folder. Runtime code uses the standard
library; pytest and Ruff are development-only tools.
