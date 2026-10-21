"""Run from the repository root; all sample files are temporary."""

from pathlib import Path
from tempfile import TemporaryDirectory

from core_mastery.strings_and_files import (
    load_notes,
    normalize_whitespace,
    parse_assignment,
    read_clean_lines,
    save_notes,
)


def main() -> None:
    """Demonstrate string transformations and a file round trip without leftovers."""
    print(normalize_whitespace("  Python\tand\nfiles  "))
    print(parse_assignment(" language = Python=3.12 "))
    with TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source.txt"
        source.write_text("  Python   basics\n\n JSON files ", encoding="utf-8")
        notes = read_clean_lines(source)
        target = root / "notes.json"
        save_notes(target, notes)
        print(load_notes(target))
        try:
            save_notes(target, ["replacement"])
        except FileExistsError:
            print("Existing notes preserved")


if __name__ == "__main__":
    main()
