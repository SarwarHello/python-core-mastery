# Python Core Mastery

Typed, tested Python exercises following a seven-day foundations roadmap.
Python 3.12+ is required; runtime code uses only the standard library.

## Setup

From the repository root on Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
```

On Linux/macOS use `python3.12 -m venv .venv` and `.venv/bin/python`.
Development versions are pinned in requirements-dev.txt; no environment activation
or global package installation is required. The src layout uses editable installation.

## Day 1: functions and type hints

[Topic guide and exercises](01_functions/README.md) explain parameters, defaults,
keyword-only arguments, return types, generics, callbacks and runtime validation.

```powershell
.venv\Scripts\python.exe 01_functions/examples.py
```

```text
250
675
['1', '2', '3']
```

## Day 2: lists, tuples, sets and dictionaries

[Topic guide and exercises](02_data_structures/README.md) cover sorted list copies,
min/max tuple results, set intersection/difference and dictionary grouping.
Existing ordered deduplication and word counting provide additional practice.

```powershell
.venv\Scripts\python.exe 02_data_structures/examples.py
.venv\Scripts\python.exe examples/collections_demo.py
```

The first example prints:

```text
[9, 7]
(2, 9)
['Python'] ['SQL']
{'backend': ['Ada', 'Sam'], 'data': ['Lin']}
```

The collections example prints:

```text
['Python', 'SQL', 'Git']
{'python': 3, 'sql': 1, 'and': 1}
```

`ordered_unique` consumes hashable items once and preserves the first occurrence.
Python equality rules apply, including `1 == True`; unhashable values raise
TypeError. `word_frequencies` supports casefolded or case-sensitive counting,
retains internal apostrophes and dictionary encounter order, and rejects invalid
argument types. Its standard-library regex tokenizer is intentionally limited;
see [the concept guide](docs/concepts.md) for Unicode and complexity notes.

## Day 3: strings and files

[Topic guide and exercises](03_strings_and_files/README.md) cover split/join,
partition/strip, pathlib, explicit UTF-8, context managers and JSON round trips.

```powershell
.venv\Scripts\python.exe 03_strings_and_files/examples.py
```

```text
Python and files
('language', 'Python=3.12')
['Python basics', 'JSON files']
Existing notes preserved
```

The example creates only temporary files and cleans up afterwards. Saving notes
uses exclusive creation; existing files are preserved. Malformed JSON, wrong
schemas, missing paths and invalid encoding have explicit error contracts.
Day 3 was completed on 21 October 2026, after its original target date.

## Day 4: OOP, inheritance and encapsulation

[Topic guide and exercises](04_oop/README.md) demonstrate constructors, instance
state, read-only properties, validated methods, super(), overriding, polymorphism
and composition through StockItem, LimitedStockItem and Inventory.

```powershell
.venv\Scripts\python.exe 04_oop/examples.py
```

```text
PEN: 4
BOX: 3
Total: 7
restock exceeds capacity
After withdrawal: 6
```

Failed operations preserve stock quantities. Inventory exposes membership snapshots
while sharing the underlying stock items intentionally. This in-memory exercise is
not thread-safe or persistent. Day 4 was completed on 30 October 2026.

## Day 5: decorators and generators

[Topic guide](05_decorators_generators/README.md) explains decorator factories,
closures, wraps, typed callable forwarding, lazy batching and running totals.

```powershell
.venv\Scripts\python.exe 05_decorators_generators/examples.py
```

```text
[(2, 5, 9), (10,)]
consume: 0.25s (illustrative clock)
First total: 1
Remaining totals: [3, 6]
Exhausted: []
```

The clock is synthetic for reproducible output. The decorator times synchronous
consumption, not creation of a lazy iterator. Tests use no sleeps. Day 5 was
completed on 8 November 2026 with three meaningful commits.

## Day 6: exceptions, logging and context managers

[Topic guide](06_error_handling/README.md) demonstrates domain exceptions with
preserved causes, structured log fields, and a context manager that publishes a
staged text file only on successful exit. Existing note parsing is reused.

```powershell
.venv\Scripts\python.exe 06_error_handling/examples.py
```

The temporary-file example loads notes, rolls back a cancelled edit, and recovers
from a missing file. Logs contain outcome metadata rather than raw notes or paths.
The guide includes exact output and filesystem limitations. Day 6 was completed on
14 November 2026 with three meaningful commits.

## Day 7: CLI task manager

[Mini-project guide](07_cli_task_manager/README.md) covers installation, commands,
storage format, error handling and limitations. After reinstalling the editable
package, run:

```powershell
.venv\Scripts\core-tasks.exe add "Review Python basics"
.venv\Scripts\core-tasks.exe list
.venv\Scripts\core-tasks.exe complete 1
```

Tasks persist in `.task-manager.json` in the current directory (ignored by Git).
Use `--file PATH` before the command to choose a file. The parent folder must exist.
`list --status open` and `list --status done` filter results. Help is available
with `--help`; module invocation also works: `python -m core_mastery.task_cli`.

For a disposable demo that does not touch your task file:

```powershell
.venv\Scripts\python.exe 07_cli_task_manager/examples.py
```

The task manager validates stored data, preserves corrupt files, and stages writes
before replacement. It is intended for one writer at a time, not concurrent use.
Day 7 was completed on 21 November 2026, finishing the foundations phase.

## Progress

Days 1–7 are implemented with 245 passing local tests. Day 2 was completed
ahead of its target date; actual work is recorded as 12 October 2026, not backdated.
See [ROADMAP.md](ROADMAP.md) and [PROGRESS.md](PROGRESS.md) for scope and evidence.

## Checks

```powershell
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m ruff format --check .
.venv\Scripts\python.exe -m pip check
```

CI runs the checks on Python 3.12 after publication. Tests describe contracts,
including boundary values, invalid types and callback errors. Type hints alone
are not runtime validation. No static type-checker pass is claimed.

Implementations live in src/core_mastery; numbered topic folders contain runnable
examples and learning guides, with tests in tests/ to avoid duplicating code.
No license has been selected. This is a learning repository, not a production service.
