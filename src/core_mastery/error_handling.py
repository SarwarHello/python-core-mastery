"""Translate expected note-loading failures and log safe outcome metadata."""

import logging
from pathlib import Path

from core_mastery.strings_and_files import load_notes

logger = logging.getLogger(__name__)


class NotesLoadError(Exception):
    """A recoverable note-loading failure; inspect __cause__ for its origin."""


def load_notes_safely(path: Path) -> list[str]:
    """Load notes, translating expected I/O/data errors without hiding defects.

    Reuse Day 3 validation. Preserve the original exception through explicit
    chaining. Logs omit paths, note text and exception messages; callers decide
    where/how logs are displayed. Original exceptions may contain sensitive
    details, so avoid blindly displaying full tracebacks to end users.
    """
    try:
        notes = load_notes(path)
    except OSError as error:
        logger.warning("notes_load_failed", extra={"failure_kind": "io"})
        raise NotesLoadError("Unable to read notes") from error
    except (ValueError, UnicodeError) as error:
        logger.warning("notes_load_failed", extra={"failure_kind": "data"})
        raise NotesLoadError(
            "Notes must contain a UTF-8 JSON array of strings"
        ) from error
    else:
        logger.info("notes_loaded", extra={"note_count": len(notes)})
        return notes
