"""Deterministic logging and context-manager example using temporary files."""

import json
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from core_mastery.context_managers import staged_text_writer
from core_mastery.error_handling import NotesLoadError, load_notes_safely


def main() -> None:
    """Configure logging at the application boundary and demonstrate recovery."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout
    )
    with TemporaryDirectory() as directory:
        target = Path(directory) / "notes.json"
        with staged_text_writer(target) as stream:
            json.dump(["Learn exceptions", "Practice cleanup"], stream)
        print(f"Notes: {load_notes_safely(target)}")
        try:
            with staged_text_writer(target) as stream:
                stream.write("incomplete")
                raise ValueError("cancel edit")
        except ValueError:
            print("Cancelled edit; previous notes preserved")
        print(f"Notes: {load_notes_safely(target)}")
        try:
            load_notes_safely(Path(directory) / "missing.json")
        except NotesLoadError as error:
            print(f"Recovered: {error}")
            print(f"Cause: {type(error.__cause__).__name__}")


if __name__ == "__main__":
    main()
