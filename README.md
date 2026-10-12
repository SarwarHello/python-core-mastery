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
