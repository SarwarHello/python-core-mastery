"""A context manager that publishes a text file only on successful exit."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TextIO


@contextmanager
def staged_text_writer(path: Path) -> Iterator[TextIO]:
    """Yield a UTF-8 writer, replacing path only after the body and close succeed.

    Stage in the destination directory so os.replace stays on one filesystem.
    Existing content survives body/replace failures; temporary files are cleaned
    in finally. Missing parent directories are not created. Existing targets are
    intentionally replaced on success, unlike Day 3's exclusive note creation.

    Replacement atomicity depends on the filesystem. No fsync/crash durability,
    metadata preservation or concurrent-writer coordination is provided. Cleanup
    failures propagate (and may become the active exception with the original
    retained as context). The caller must not move/delete the temporary file.
    """
    temporary = NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary_path = Path(temporary.name)
    try:
        with temporary as stream:
            yield stream
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
