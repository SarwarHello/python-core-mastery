# Day 6 - exceptions, logging and context managers

[Error handling source](../src/core_mastery/error_handling.py) and
[tests](../tests/test_error_handling.py); [context manager source](../src/core_mastery/context_managers.py)
and [tests](../tests/test_context_managers.py).

```powershell
.venv\Scripts\python.exe 06_error_handling/examples.py
```

Expected output:

```text
INFO notes_loaded
Notes: ['Learn exceptions', 'Practice cleanup']
Cancelled edit; previous notes preserved
INFO notes_loaded
Notes: ['Learn exceptions', 'Practice cleanup']
WARNING notes_load_failed
Recovered: Unable to read notes
Cause: FileNotFoundError
```

The demo uses temporary files and cleans up after itself. No personal files or
network services are needed.

## Exceptions and recovery

`load_notes_safely` reuses Day 3's parser/validation instead of duplicating it.
Expected filesystem and data errors become NotesLoadError. `raise ... from error`
keeps the original exception in __cause__, allowing callers to diagnose the cause
while presenting a stable message. Unexpected programming errors such as TypeError
propagate rather than being disguised as empty notes or a recoverable load failure.

The try block contains only the operation being translated. The else block logs
successful completion; failures in unrelated success handling are not caught by
those except clauses. Narrow catches prevent hiding defects. The example catches
the domain error at the application boundary and continues deliberately.

## Logging

Library code uses `logging.getLogger(__name__)`, without adding handlers or changing
global logging configuration. The executable example configures a simple stdout
handler with basicConfig. INFO records a successful load with a note_count field;
WARNING records an expected failure with failure_kind (`io` or `data`). The custom
fields are available on LogRecord and need a formatter to display them.

Paths, payloads and exception messages are not included in log messages, and no
traceback is attached. Chained exceptions can still contain private details:
applications must decide whether and where to display them. Tests capture logs
with caplog. No blanket exception suppression or automatic retry is introduced.

## Context-manager lifecycle

`staged_text_writer` uses @contextmanager and yield to divide setup from teardown:

1. Create a temporary UTF-8 text file in the destination directory.
2. Yield its stream to the with body.
3. On normal exit, close the stream and replace the destination with os.replace.
4. On body, close or replacement failure, skip publication; finally removes the
   temporary path. Body exceptions are not suppressed. A setup failure prevents
   the body from running at all.

The existing destination stays unchanged until replacement. Using the same parent
keeps staging and destination on one filesystem. Closing before replacement also
supports Windows file-handle rules. This differs intentionally from Day 3's
save_notes, which rejects an existing destination instead of replacing it.

Replacement atomicity depends on filesystem semantics; this is not crash-durable
storage (no fsync), permission/metadata preservation, or concurrent-write control.
The last successful writer wins. Keep the working directory stable when supplying
relative paths. Do not delete/move the staging file inside the with body. Cleanup
can itself fail and become the active exception, with the earlier error retained
as exception context. Those failures are not silently ignored.

## Verification and interview review

Tests cover chained causes, data versus I/O failures, unexpected programming
errors, safe log fields, successful publication, preservation on failure,
UTF-8 errors, missing parents, closed handles and temporary-file cleanup.
Permission/replacement failures are injected for cross-platform reliability.
The streaming writer uses disk space proportional to output; note loading keeps
parsed data in memory. No third-party dependency is added.

Explain: why not catch Exception everywhere? How do cause and context differ?
Why configure logging at the entry point? When does finally execute? What happens
if an exception is raised inside the with body or during resource acquisition?
