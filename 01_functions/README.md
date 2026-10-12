# Day 1 — functions and type hints

Implementation: [functions_lab.py](../src/core_mastery/functions_lab.py).
Tests: [test_functions_lab.py](../tests/test_functions_lab.py).
Run `.venv\Scripts\python.exe 01_functions/examples.py` from the repository root.

Expected output:

```text
250
675
['1', '2', '3']
```

## Exercises and explanations

1. `calculate_total`: positional arguments, a default quantity, keyword-only
   discount and an integer return value. Prices use integer pence so floating
   point is unnecessary. The final amount rounds down; this is a teaching
   contract, not a production billing policy. Zero quantity and 100% discount
   are valid; negative values, bools and non-integers are rejected.
2. `transform_values`: a generic higher-order function accepts an iterable and a
   callable, returning a list whose type may differ from the input type. The
   callback runs once per value, in order. Callback errors propagate.

Type annotations describe intended types but do not enforce them at runtime.
The first function demonstrates explicit runtime validation; the second follows
its typed contract without trying to validate arbitrary callable signatures.
Mutable default arguments are avoided: a shared default list would retain state
across calls. Return values make functions testable without capturing print output.

`calculate_total` uses a fixed number of arithmetic operations (integer cost grows
with integer size). Transformation is O(n) plus callback work and stores O(n)
results. Reusable implementation stays under src; topic folders provide navigation
and examples, avoiding copied exercise implementations.

Review: explain positional versus keyword-only arguments, default values, a return
annotation, why `bool` needs special handling, and how T/U describe transformations.
