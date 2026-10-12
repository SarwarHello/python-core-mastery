# Day 2 — lists, tuples, sets and dictionaries

Implementation: [data_structures.py](../src/core_mastery/data_structures.py) and
[collections_lab.py](../src/core_mastery/collections_lab.py).
Tests: [test_data_structures.py](../tests/test_data_structures.py) and
[test_collections_lab.py](../tests/test_collections_lab.py).
Run `.venv\Scripts\python.exe 02_data_structures/examples.py` from the root.

Expected output:

```text
[9, 7]
(2, 9)
['Python'] ['SQL']
{'backend': ['Ada', 'Sam'], 'data': ['Lin']}
```

| Type | Exercise | Behaviour and tradeoff |
| --- | --- | --- |
| list | top_scores | Mutable sequence; sorted returns a new list; duplicates stay; O(n log n) time, O(n) space |
| tuple | score_bounds | Fixed ordered pair returned for unpacking; tuple slots are immutable; one-pass O(n) time, O(1) extra space |
| set | compare_skills | Membership, intersection and difference; unique values, no display-order guarantee; fresh result sets |
| dict | group_members | Department keys map to independent lists; insertion order preserved; expected O(n) time and O(n) result space |

For sets, intersection is expected O(min(r,a)); difference is O(r), where r and a
are the input sizes. Hash-operation complexities assume typical hash behaviour.

Existing ordered_unique combines a set and list to retain first occurrences;
word_frequencies demonstrates dictionary counting. These are reused, not rewritten.
A tuple is not deeply immutable if it holds mutable objects. A shallow list copy
also keeps references to its elements. Tests prove these exercises preserve input
collections and avoid accidentally sharing one department's list with another.

Follow the annotated input types; only documented boundary validation is performed.
Skill matching is case-sensitive. Duplicate member names are retained because the
contract is grouping, not deduplication. Display sets using sorted() in examples
so output is reproducible. See docs/concepts.md for the word-tokenizer limitations.
