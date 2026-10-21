# Day 3 — string manipulation and file handling

[Implementation](../src/core_mastery/strings_and_files.py) ·
[Tests](../tests/test_strings_and_files.py)

Run from the repository root:

```powershell
.venv\Scripts\python.exe 03_strings_and_files/examples.py
```

Expected output (the example uses and cleans up temporary files):

```text
Python and files
('language', 'Python=3.12')
['Python basics', 'JSON files']
Existing notes preserved
```

## Exercises

| Function | Concepts | Contract |
| --- | --- | --- |
| normalize_whitespace | split/join, immutable strings | Trim and collapse Unicode whitespace; preserve case/punctuation |
| parse_assignment | partition/strip, tuple unpacking | Split only at the first equals sign; require a key; permit an empty value |
| read_clean_lines | pathlib, iteration, context managers | Read UTF-8, normalize each line, skip blanks |
| save_notes | JSON serialization, exclusive creation | Create a new UTF-8 JSON array of strings; never overwrite an existing file |
| load_notes | JSON parsing and schema validation | Return a list of strings; reject malformed JSON and other shapes |

Strings are immutable: transformations return new values. `partition` retains
additional equals signs, unlike unrestricted splitting. `split()` without a
separator recognizes whitespace runs including tabs/newlines and nonbreaking
spaces. No case folding or Unicode normalization is performed here.

Explicit UTF-8 avoids dependence on the operating system's default encoding.
Context managers close file handles even when decoding/parsing fails. Use Path
objects instead of manual platform-specific path concatenation. The JSON library
handles quotes, newlines and Unicode; never construct JSON by concatenating text.

Validation happens before the destination is opened. Mode `x` fails if the file
already exists, avoiding a race-prone exists-then-write check. Parent directories
are not created implicitly. Writing is **not crash-atomic**: interruption or disk
failure can leave a partial newly created file. This example is for small files;
JSON and returned results are held in memory. Text scanning is O(n); memory grows
with the returned content. Parsing/serialization costs grow with file size.

## Failure cases and tests

Missing paths raise FileNotFoundError; invalid UTF-8 raises UnicodeDecodeError;
malformed JSON raises JSONDecodeError; a wrong JSON shape raises ValueError.
Permission and other OS errors propagate instead of being disguised as empty data.
Inputs follow the annotated string/Path contracts; JSON structure is explicitly
validated because loaded data is untrusted.

Tests use pytest temporary directories, never personal files. They cover Unicode,
mixed newlines, empty content, assignment errors, round trips, malformed data,
existing-file preservation, missing parents and file-handle release.

Review: why use `partition` instead of `split('=')`? Why set an encoding? What is
the difference between a syntax error and a valid JSON object of the wrong shape?
Why does exclusive creation protect existing files but not make a write atomic?
