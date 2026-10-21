"""String transformations and explicit UTF-8 file contracts."""

import json
from pathlib import Path


def normalize_whitespace(text: str) -> str:
    """Strip surrounding Unicode whitespace and collapse internal runs to spaces.

    Preserve letter case and punctuation. Follow the annotated string contract.
    """
    return " ".join(text.split())


def parse_assignment(text: str) -> tuple[str, str]:
    """Split at the first equals sign, trim each side and require a nonempty key.

    Empty values and further equals signs in the value are valid. Internal spaces
    are preserved. Raise ValueError for a missing separator or blank key.
    """
    key, separator, value = text.partition("=")
    if not separator:
        raise ValueError("assignment must contain '='")
    key = key.strip()
    if not key:
        raise ValueError("assignment key must not be empty")
    return key, value.strip()


def read_clean_lines(path: Path) -> list[str]:
    """Read UTF-8 text, normalize whitespace per line and omit blank lines.

    Open files with a context manager. FileNotFoundError, UnicodeDecodeError and
    other I/O errors propagate so the caller can distinguish failure causes.
    """
    with path.open("r", encoding="utf-8") as stream:
        return [clean for line in stream if (clean := normalize_whitespace(line))]


def _validate_notes(value: object) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(note, str) for note in value):
        raise ValueError("notes must be a JSON array of strings")
    return value


def save_notes(path: Path, notes: list[str]) -> None:
    """Create a UTF-8 JSON file containing string notes without overwriting.

    Validate and serialize before opening the destination. Existing files raise
    FileExistsError; absent parent directories and other I/O errors propagate.
    Creation is exclusive but writing is not crash-atomic; interrupted writes may
    leave an incomplete new file. This small exercise keeps all notes in memory.
    """
    payload = json.dumps(_validate_notes(notes), ensure_ascii=False, indent=2) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(payload)


def load_notes(path: Path) -> list[str]:
    """Load a UTF-8 JSON array of strings; reject malformed or mismatched data.

    Invalid JSON raises JSONDecodeError (a ValueError subclass); a wrong data
    shape raises ValueError. Filesystem and decoding errors propagate unchanged.
    """
    with path.open("r", encoding="utf-8") as stream:
        return _validate_notes(json.load(stream))
