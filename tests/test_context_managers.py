"""File publication, rollback, cleanup and exception propagation."""

from pathlib import Path

import pytest

from core_mastery import context_managers
from core_mastery.context_managers import staged_text_writer


def test_new_file_published_only_after_exit(tmp_path):
    target = tmp_path / "notes.txt"
    with staged_text_writer(target) as stream:
        stream.write("Café\n")
        assert not target.exists()
        assert Path(stream.name).parent == target.parent
    assert stream.closed
    assert target.read_bytes() == "Café\n".encode()
    assert list(tmp_path.iterdir()) == [target]


def test_success_replaces_existing_file(tmp_path):
    target = tmp_path / "notes.txt"
    target.write_text("old", encoding="utf-8")
    with staged_text_writer(target) as stream:
        stream.write("new")
        stream.flush()
        assert target.read_text(encoding="utf-8") == "old"
    assert target.read_text(encoding="utf-8") == "new"
    assert list(tmp_path.iterdir()) == [target]


@pytest.mark.parametrize("exists", [False, True])
def test_body_failure_preserves_target_and_cleans_up(tmp_path, exists):
    target = tmp_path / "notes.txt"
    if exists:
        target.write_text("old", encoding="utf-8")
    error = ValueError("body failed")
    with pytest.raises(ValueError) as caught, staged_text_writer(target) as stream:
        stream.write("partial")
        raise error
    assert caught.value is error
    assert stream.closed
    assert target.exists() is exists
    if exists:
        assert target.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.iterdir()) == ([target] if exists else [])


def test_replace_failure_preserves_original_and_cleans(tmp_path, monkeypatch):
    target = tmp_path / "notes.txt"
    target.write_text("old", encoding="utf-8")
    error = PermissionError("replace denied")

    def fail(source, destination):
        assert Path(source).parent == target.parent
        assert destination == target
        raise error

    monkeypatch.setattr(context_managers.os, "replace", fail)
    with pytest.raises(PermissionError) as caught, staged_text_writer(target) as stream:
        stream.write("new")
    assert caught.value is error
    assert stream.closed
    assert target.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.iterdir()) == [target]


def test_missing_parent_fails_before_entering_body(tmp_path):
    target = tmp_path / "missing" / "notes.txt"
    with pytest.raises(FileNotFoundError), staged_text_writer(target):
        pytest.fail("body must not run")
    assert list(tmp_path.iterdir()) == []


def test_empty_body_creates_empty_file(tmp_path):
    target = tmp_path / "empty.txt"
    with staged_text_writer(target):
        pass
    assert target.read_bytes() == b""


def test_base_exception_is_not_suppressed_and_still_cleans(tmp_path):
    target = tmp_path / "notes.txt"
    with pytest.raises(KeyboardInterrupt), staged_text_writer(target) as stream:
        stream.write("partial")
        raise KeyboardInterrupt
    assert stream.closed
    assert list(tmp_path.iterdir()) == []


def test_unicode_encoding_failure_does_not_publish(tmp_path):
    target = tmp_path / "notes.txt"
    with pytest.raises(UnicodeEncodeError), staged_text_writer(target) as stream:
        stream.write("\ud800")
    assert stream.closed
    assert list(tmp_path.iterdir()) == []


def test_nested_writers_for_different_files_are_independent(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    with staged_text_writer(first) as outer:
        outer.write("one")
        with staged_text_writer(second) as inner:
            inner.write("two")
        assert second.read_text() == "two"
        assert not first.exists()
    assert first.read_text() == "one"
    assert set(tmp_path.iterdir()) == {first, second}
