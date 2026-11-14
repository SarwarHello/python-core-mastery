"""Expected errors, exception chaining and logs without raw input details."""

import json
import logging

import pytest

from core_mastery import error_handling
from core_mastery.error_handling import NotesLoadError, load_notes_safely


@pytest.mark.parametrize("notes", [[], ["one", "two"]])
def test_success_and_structured_count(tmp_path, caplog, notes):
    path = tmp_path / "notes.json"
    path.write_text(json.dumps(notes), encoding="utf-8")
    with caplog.at_level(logging.INFO, logger=error_handling.__name__):
        assert load_notes_safely(path) == notes
    record = caplog.records[-1]
    assert record.getMessage() == "notes_loaded"
    assert record.note_count == len(notes)
    assert record.levelno == logging.INFO


def test_missing_file_keeps_original_cause(tmp_path, caplog):
    with pytest.raises(NotesLoadError, match="Unable to read") as caught:
        load_notes_safely(tmp_path / "missing.json")
    assert isinstance(caught.value.__cause__, FileNotFoundError)
    assert caplog.records[-1].failure_kind == "io"


@pytest.mark.parametrize("payload", ["{", "null", "{}", "[1]", '["ok", null]'])
def test_invalid_data_is_translated(tmp_path, caplog, payload):
    path = tmp_path / "notes.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(NotesLoadError, match="array of strings") as caught:
        load_notes_safely(path)
    assert isinstance(caught.value.__cause__, ValueError)
    assert caplog.records[-1].failure_kind == "data"


def test_invalid_encoding_keeps_decoding_cause(tmp_path):
    path = tmp_path / "notes.json"
    path.write_bytes(b"\xff")
    with pytest.raises(NotesLoadError) as caught:
        load_notes_safely(path)
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_permission_failure_keeps_same_cause(monkeypatch, tmp_path):
    original = PermissionError("private path detail")

    def fail(path):
        raise original

    monkeypatch.setattr(error_handling, "load_notes", fail)
    with pytest.raises(NotesLoadError) as caught:
        load_notes_safely(tmp_path / "notes.json")
    assert caught.value.__cause__ is original


def test_programming_error_is_not_disguised(monkeypatch, tmp_path, caplog):
    original = TypeError("programming defect")

    def fail(path):
        raise original

    monkeypatch.setattr(error_handling, "load_notes", fail)
    with pytest.raises(TypeError) as caught:
        load_notes_safely(tmp_path / "notes.json")
    assert caught.value is original
    assert not caplog.records


def test_logs_do_not_expose_path_payload_or_traceback(tmp_path, caplog):
    path = tmp_path / "private-name.json"
    path.write_text("private-payload", encoding="utf-8")
    with pytest.raises(NotesLoadError):
        load_notes_safely(path)
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.WARNING
    assert record.getMessage() == "notes_load_failed"
    assert record.exc_info is None
    assert "private" not in caplog.text


def test_success_log_does_not_include_notes(tmp_path, caplog):
    path = tmp_path / "notes.json"
    path.write_text('["private-payload"]', encoding="utf-8")
    with caplog.at_level(logging.INFO, logger=error_handling.__name__):
        load_notes_safely(path)
    assert "private-payload" not in caplog.text
