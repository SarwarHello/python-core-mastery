"""String contracts and file behaviour using isolated temporary directories."""

import json

import pytest

from core_mastery.strings_and_files import (
    load_notes,
    normalize_whitespace,
    parse_assignment,
    read_clean_lines,
    save_notes,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        (" \t\n", ""),
        ("  Python\tand\nSQL  ", "Python and SQL"),
        ("Café\u00a0API!", "Café API!"),
        ("already clean", "already clean"),
    ],
)
def test_normalize_whitespace(text, expected):
    result = normalize_whitespace(text)
    assert result == expected
    assert normalize_whitespace(result) == result


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (" language = Python ", ("language", "Python")),
        ("key=a=b", ("key", "a=b")),
        ("key=", ("key", "")),
        ("full name = Ada  Lovelace", ("full name", "Ada  Lovelace")),
    ],
)
def test_parse_assignment(text, expected):
    assert parse_assignment(text) == expected


@pytest.mark.parametrize("text", ["", "missing separator", "=value", " \t = x"])
def test_invalid_assignment(text):
    with pytest.raises(ValueError):
        parse_assignment(text)


def test_read_clean_lines_mixed_newlines_and_unicode(tmp_path):
    path = tmp_path / "input.txt"
    path.write_bytes("  Café\tAPI \r\n\r\n  Python  SQL\nlast".encode())
    original = path.read_bytes()
    assert read_clean_lines(path) == ["Café API", "Python SQL", "last"]
    assert path.read_bytes() == original
    # Rename also checks that the reader released its handle on Windows.
    path.rename(tmp_path / "renamed.txt")


def test_empty_text_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.touch()
    assert read_clean_lines(path) == []


@pytest.mark.parametrize("reader", [read_clean_lines, load_notes])
def test_missing_file(tmp_path, reader):
    with pytest.raises(FileNotFoundError):
        reader(tmp_path / "missing.txt")


@pytest.mark.parametrize("reader", [read_clean_lines, load_notes])
def test_invalid_utf8(tmp_path, reader):
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"\xff")
    with pytest.raises(UnicodeDecodeError):
        reader(path)


@pytest.mark.parametrize(
    "notes", [[], [""], ["Café", "line\nbreak", 'a "quote"', "日本語"]]
)
def test_notes_round_trip(tmp_path, notes):
    path = tmp_path / "notes.json"
    before = notes.copy()
    assert save_notes(path, notes) is None
    assert load_notes(path) == notes
    assert notes == before
    assert json.loads(path.read_text(encoding="utf-8")) == notes
    assert path.read_bytes().endswith(b"\n")


def test_existing_destination_is_preserved(tmp_path):
    path = tmp_path / "notes.json"
    path.write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        save_notes(path, ["replacement"])
    assert path.read_text(encoding="utf-8") == "original"


@pytest.mark.parametrize("notes", [None, "text", {"note": "text"}, [1], ["ok", None]])
def test_invalid_notes_do_not_create_destination(tmp_path, notes):
    path = tmp_path / "notes.json"
    with pytest.raises(ValueError, match="array of strings"):
        save_notes(path, notes)
    assert not path.exists()


@pytest.mark.parametrize("payload", ["{}", "null", '"text"', "[1]", '["ok", null]'])
def test_load_rejects_wrong_shape(tmp_path, payload):
    path = tmp_path / "notes.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(ValueError, match="array of strings"):
        load_notes(path)


@pytest.mark.parametrize("payload", ["", "[", '["ok",]', '["ok"] trailing'])
def test_load_rejects_malformed_json(tmp_path, payload):
    path = tmp_path / "notes.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_notes(path)
    path.rename(tmp_path / "closed.json")


def test_missing_parent_is_not_created(tmp_path):
    path = tmp_path / "missing" / "notes.json"
    with pytest.raises(FileNotFoundError):
        save_notes(path, ["hello"])
    assert not path.parent.exists()
