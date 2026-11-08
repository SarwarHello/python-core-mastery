# Day 5 - decorators and generators

[Decorator source](../src/core_mastery/decorators.py) and
[tests](../tests/test_decorators.py); [generator source](../src/core_mastery/generators.py)
and [tests](../tests/test_generators.py).

```powershell
.venv\Scripts\python.exe 05_decorators_generators/examples.py
```

Expected output:

```text
[(2, 5, 9), (10,)]
consume: 0.25s (illustrative clock)
First total: 1
Remaining totals: [3, 6]
Exhausted: []
```

## Decorator exercise

`timed(report, *, clock=perf_counter)` is a decorator factory: the outer function
captures configuration in a closure, the middle accepts a function, and the
wrapper measures successful calls. `@timed(report)` is equivalent to assigning
`function = timed(report)(function)`.

functools.wraps preserves name, docstring, annotations and __wrapped__, allowing
inspect.signature to follow the original signature. The P/R type parameters
forward argument and return types; annotations do not enforce runtime types.
Positional/keyword arguments and the original return object are preserved.

Wrapped exceptions propagate unchanged without a report. Clock/report failures
also propagate, and a reporting failure can occur after the function has performed
side effects. Callbacks follow their annotated contracts. Named synchronous
functions and methods are supported, not arbitrary callable objects.

The default perf_counter is monotonic; injected clocks should provide monotonic
seconds. The example's 0.25s is synthetic, not a benchmark. Direct async/generator
functions are rejected because their creation is not their execution. A normal
function returning an iterator is timed only until return: decorate a function
that consumes it to measure iteration, as shown. Arbitrary wrappers may hide an
async/generator function from introspection. No argument values are reported.

## Generator exercises

- `batches(values, size)` immediately validates a positive integer size, excluding
  bool. It returns a generator that acquires/consumes input only on iteration.
  Each next() reads at most size elements. Partial final tuples are retained;
  input errors propagate without yielding an incomplete failing batch. Source
  ownership stays with the caller: closing the wrapper does not close input.
- `running_totals(values, *, start=0)` yields after each addition. Empty input
  yields nothing, even with a nonzero start. Follow its annotated integer contract.
  It composes with batching without creating an intermediate full list.

`yield` suspends execution and retains local state. Iterators are one-shot; list()
after exhaustion returns an empty list. A fresh iterator over a reusable list is
different from reusing an exhausted iterator. Laziness supports infinite inputs
with bounded consumers; list() on an infinite source never completes.

Batching uses O(size) temporary space; running totals keep O(1) accumulator state,
ignoring growing integer size. Both do O(n) iteration work on finite input.
Retaining every result (as the small example does) costs O(n) caller memory.
Python 3.12's itertools.batched and itertools.accumulate are standard alternatives;
these explicit implementations teach validation timing and suspended execution.

## Review and verification

Tests cover metadata/signature, return identity, errors, methods, repeated calls,
unsupported function kinds, eager size validation, lazy iterator acquisition,
no read-ahead, partial batches, bounded consumption of infinite sources,
exhaustion, source failures and composed pipelines. No sleeps or timing thresholds.

Explain: why wraps? What does a closure retain? When does a generator body run?
Why is timing generator creation misleading? Why can list() defeat streaming?
