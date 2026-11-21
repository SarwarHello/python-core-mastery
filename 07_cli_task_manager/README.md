# Day 7 - CLI task manager

A small, persistent task manager that combines functions, type hints, immutable
objects, collections, JSON, exceptions and context managers from Days 1-6.
Runtime dependencies: Python standard library only. No service or account needed.

[Task model/store](../src/core_mastery/task_store.py) ·
[CLI](../src/core_mastery/task_cli.py) ·
[Storage tests](../tests/test_task_store.py) ·
[CLI tests](../tests/test_task_cli.py)

## Install and run

From the repository root, install the package so the console command is generated:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
.venv\Scripts\core-tasks.exe --help
.venv\Scripts\core-tasks.exe add "Review Python basics"
.venv\Scripts\core-tasks.exe list
.venv\Scripts\core-tasks.exe complete 1
.venv\Scripts\core-tasks.exe list --status done
```

Alternatively use `.venv\Scripts\python.exe -m core_mastery.task_cli` followed by
the same arguments. On Linux/macOS use `.venv/bin/python` and `.venv/bin/core-tasks`.
The commands create local task data, not Git commits.

Storage defaults to `.task-manager.json` in the current working directory. That
filename is ignored by Git. To choose another file, put the global option before
the subcommand: `core-tasks --file path/to/tasks.json add "Read docs"`. The parent
folder must exist; custom files outside the default name need their own ignore
rule if kept in a repository. Do not use personal or confidential notes in demos.

## Commands and outcomes

| Command | Behaviour |
| --- | --- |
| add "title" | Normalize whitespace, create an open task, print its assigned ID |
| list | Show all tasks in creation order using [ ] / [x] markers |
| list --status open | Show only incomplete tasks |
| list --status done | Show only completed tasks |
| complete ID | Mark complete; repeating is a successful no-op |
| --help | Show usage without reading or creating storage |

Exit 0 means success, exit 1 an expected data/storage/domain failure, and exit 2
invalid command syntax. Expected errors go to stderr without a traceback. Empty
or unmatched lists print `No tasks found.` Titles must normalize to 1-200 printable
characters; terminal escape/control characters are rejected. Quote multiword titles.
IDs are positive integers assigned as max existing ID + 1; deletion is not included.

## Safe demonstration

```powershell
.venv\Scripts\python.exe 07_cli_task_manager/examples.py
```

This runs separate processes against temporary storage and cleans it up afterwards:

```text
Added task 1: Review Python basics
Added task 2: Write CLI tests
[ ] 1: Review Python basics
[ ] 2: Write CLI tests
Completed task 1: Review Python basics
[ ] 2: Write CLI tests
[x] 1: Review Python basics
```

## Design and data format

The CLI parses arguments and presents outcomes. TaskStore handles operations and
persistence. Frozen Task objects are validated snapshots, not mutable shared state.
The store reuses Day 6's staged_text_writer rather than copying file-update logic.

```json
{
  "version": 1,
  "tasks": [
    {"id": 1, "title": "Review Python basics", "completed": false}
  ]
}
```

The loader validates version, field names/types, IDs, titles, completion flags and
ID uniqueness. Missing files mean an empty store; an existing empty/corrupt file
is an error, never silently reset. Fix or restore a corrupted file from a backup;
do not expect this program to recover damaged data automatically. Error chaining
preserves underlying causes for debugging without printing them to end users.

Writes are staged beside the destination, then replaced after success. Failure
before replacement preserves existing bytes. This is a small single-user learning
application: no locking, concurrent-update protection, fsync/crash durability,
backups, authentication, timestamps, due dates or delete command. Concurrent
processes may lose updates; run one modifying command at a time. Use a trusted,
regular local file path. JSON and output lists reside in memory; reads/updates are
O(n) in task count plus serialized content size.

## Verification and interview prompts

Tests cover persistence across separate processes, the installed console entry
point, read-only list/help, status filters, immutable snapshots, input validation,
idempotent completion, unknown IDs, invalid schemas/encoding, failed replacement
and preservation of corrupted data. No test reads or writes personal task files.

Explain the CLI/store separation, why frozen snapshots help, why a temporary
write is better than truncating in place, why atomic replacement does not prevent
lost concurrent updates, and why malformed data must not become an empty list.
