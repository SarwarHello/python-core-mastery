# Progress

Actual work date: 12 October 2026 (Europe/London).

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

## Validation

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
Day 2: this progress entry accompanies the collections/learning-material commit.
The commit containing this file can be identified from Git history; its hash is
not inserted into itself. At this snapshot, final push and remote CI verification
are pending; their outcomes will be reported in the workspace execution log.

Local authentication was verified as SarwarHello. The email-list API returned 404
with the credential's available scopes, so the repository uses GitHub's documented
ID-based noreply address for the verified account instead. Global Git settings
were not changed. Environment, caches and build metadata are ignored; staged
content was reviewed for unintended files and common secret patterns.

## Next step

Day 3: string manipulation and file handling with temporary-file tests and clear
failure handling. Await the user's next instruction.
