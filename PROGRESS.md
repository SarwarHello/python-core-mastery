# Progress

Last updated: 21 November 2026 (Europe/London). Days 1–2 were completed on 12 October; Day 3 on 21 October.

## Completed scope

- Day 1: installable Python 3.12+ package, isolated development environment,
  parameters/defaults/keyword-only arguments, return types, generics, callable
  transformation, runtime validation, guide, examples and 19 function tests.
- Day 2: lists (sorted copies), tuples (one-pass bounds), sets (skill comparison),
  dictionaries (ordered grouping), input preservation and edge cases: 18 tests.
  Existing ordered deduplication/word counting contributes another 28 tests.
- Numbered topic folders match the supplied learning roadmap. Implementation and
  tests remain centralized so examples do not duplicate logic.

Day 2 was completed ahead of its 13 October target. Both days' actual work and
commits are on 12 October; no timestamps are backdated. The earlier assistant
roadmap was corrected before this completion.

## Days 1–2 validation (historical)

All commands used the project virtual environment on Windows with Python 3.12.0.

| Check | Result |
| --- | --- |
| pytest | 65 passed, 0 failed, 0 skipped |
| Ruff check | Passed |
| Ruff format --check | Passed |
| Day 1 example | Matches its topic README |
| Day 2 example | Matches its topic README |
| Collections example | Matches root README |
| pip check | No broken requirements |
| Editable installation | Verified during initial setup |

Tools: pytest 9.1.1, Ruff 0.17.0, setuptools 84.0.0; exact development dependency
versions are in requirements-dev.txt. Type annotations are present; a static type
checker has not been configured or claimed to pass. CI repeats checks on Ubuntu
Python 3.12; its actual remote result must be checked separately after pushing.

## Git publication record

Repository: https://github.com/SarwarHello/python-core-mastery (public, user-owned).
The user explicitly authorized repository creation, commits and pushes.
Day 1 commit: `328f89f` (project foundation and typed function exercises).
Day 2 commit: `000b463`. Both commits were pushed and GitHub Actions succeeded:
https://github.com/SarwarHello/python-core-mastery/actions/runs/38188922145

Local authentication was verified as SarwarHello. The email-list API returned 404
with the credential's available scopes, so the repository uses GitHub's documented
ID-based noreply address for the verified account instead. Global Git settings
were not changed. Environment, caches and build metadata are ignored; staged
content was reviewed for unintended files and common secret patterns.

## Day 3 — strings and files

Completed on 21 October 2026 (original target 14 October; no backdating).

- Added normalize_whitespace, parse_assignment, read_clean_lines, save_notes and
  load_notes with typed interfaces and documented input/error contracts.
- Added numbered topic guide and a deterministic temporary-directory example;
  CI now runs the new example as well as the previous examples.
- Added 38 tests for string cases, Unicode, mixed newlines, JSON round trips,
  missing files, invalid encoding/schema/JSON, no-overwrite behaviour and missing
  parents. All file tests use isolated temporary directories.
- Validation: 103 tests passed (0 failures/skips), Ruff lint and formatting passed,
  Day 3 example matched documentation, pip check found no broken requirements.
  One redundant encode argument was corrected after the first lint run.
- Limitations: reads/JSON results use memory proportional to content; exclusive
  creation prevents overwriting but writes are not crash-atomic. No new dependencies.
- This entry accompanies the Day 3 implementation commit. Push and remote CI
  results are recorded separately in the central workspace log after publication.

## Day 4 — OOP, inheritance and encapsulation

Completed on 30 October 2026 (original target 15 October; no backdating).

- Added StockItem with constructor validation, per-instance state, read-only public
  properties and validated restock/withdraw methods.
- Added LimitedStockItem demonstrating super(), overriding and inherited methods;
  the base restock contract explicitly allows storage-policy rejection.
- Added Inventory to demonstrate composition, unique SKU membership, independent
  containers, live totals and shallow membership snapshots.
- Added numbered guide and deterministic example; CI runs the new example.
- Validation: 38 new tests; 141 tests passed, 0 failed/skipped. Ruff lint and format
  passed, example output matched README, pip check reported no broken requirements.
- No new dependencies. Underscore attributes are conventions, not a security
  boundary; the model is not persistent or safe for concurrent mutation.
- This entry accompanies the Day 4 implementation commit. Push and remote CI
  outcomes are recorded in the central workspace log after publication.

Day 3 publication was verified previously: commit `9a85d9f`, successful CI at
https://github.com/SarwarHello/python-core-mastery/actions/runs/39678155417.

## Day 5 - decorators and generators

Completed 8 November 2026 (original target 16 October; no backdating).

- Added typed timed decorator factory with wraps, an injected clock and reporting
  callback. Preserves arguments, return objects and metadata; rejects direct
  generator/async functions. Eleven deterministic tests cover its contracts.
- Added lazy batches and running_totals with 23 tests for validation timing,
  one-pass iteration, read-ahead bounds, partial batches, source errors and
  bounded consumption of an infinite source.
- Added numbered learning guide and integrated example; CI runs the example.
- Validation: 175 tests passed, 0 failures/skips; Ruff lint/format passed; example
  output matched; pip check passed. No new dependencies or timing-based assertions.
- Three meaningful commits requested: e98214f (tested decorator), e11d57b (tested
  generators), and the commit containing this integration/documentation entry.
- A shell startup error interrupted the first documentation attempt before files
  were created. Retried with Windows PowerShell successfully; no code/test failure.
- Timing reports successful synchronous calls only; callback failures propagate.
  Generators do not own/close their sources; retaining results uses caller memory.
- Push and remote CI verification are recorded in the central workspace log.

Day 4 push and CI succeeded: commit 50a427f; run
https://github.com/SarwarHello/python-core-mastery/actions/runs/41143959811.

## Day 6 - exceptions, logging and context managers

Completed 14 November 2026 (original target 17 October; no backdating).

- Added NotesLoadError and load_notes_safely, reusing Day 3 parsing. Expected I/O
  and data errors are chained; unexpected programming errors propagate unchanged.
  Logs expose safe outcome/count/category fields, without raw note text or paths.
- Added staged_text_writer: same-directory temporary file, close before replacement,
  publication on success, rollback/cleanup on failure, no exception suppression.
- Added numbered guide and integrated example; CI now runs the example.
- Validation: 13 exception/logging tests and 10 context-manager tests added;
  198 passed, 0 failed/skipped overall. Ruff lint/format passed; example output
  matched the guide; pip check passed. No new dependencies.
- Commits: b354dcf (errors/logging), cfce740 (context manager), and this commit
  (learning guide, integrated example, CI and progress).
- Limits: no crash durability, metadata preservation or concurrent-writer control;
  cleanup failures propagate. Chained causes may contain private details even
  though the emitted log messages omit them.
- Push and remote CI results are recorded in the central workspace log.

Day 5 publication verified: e98214f, e11d57b and 612f0af; successful CI at
https://github.com/SarwarHello/python-core-mastery/actions/runs/42445126938.

## Day 7 - CLI task manager

Completed 21 November 2026 (original target 18 October; no backdating).

- Added immutable validated Task snapshots and a versioned JSON TaskStore with
  persistent IDs, add/list/complete, idempotent completion and schema validation.
- Added argparse CLI, core-tasks console entry point, module invocation, status
  filters, help and clear stderr/exit-code contracts. Default local data is ignored.
- Reused Day 6 staged writes; corrupt stores and failed updates preserve prior data.
- Added numbered mini-project guide, disposable subprocess demo and CI step.
- Validation: 28 storage tests + 19 CLI tests added; 245 tests passed overall,
  no failures/skips. Ruff lint/format passed; demo matched; pip check passed.
  Editable reinstall and installed console entry point verified. No new dependencies.
- Commits: 62521bd (model/storage), 847bac8 (CLI and process tests), and this commit
  (guide, safe demonstration, CI and tracking).
- Limitations: in-memory JSON, trusted local file, one writer at a time; no locking,
  backup/recovery, fsync/crash durability, deletion, dates or authentication.
- Push and remote CI verification are recorded in the central workspace log.

Day 6 publication verified: b354dcf, cfce740 and 2f6f50c; successful CI at
https://github.com/SarwarHello/python-core-mastery/actions/runs/43546595574.

## Next step

Day 8: arrays and two pointers in python-dsa-challenges. Await user instruction;
that repository has not been created as part of Day 7.
