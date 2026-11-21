"""Persistent state and corrupt-data protection using temporary files."""

import json
from dataclasses import FrozenInstanceError

import pytest

from core_mastery import context_managers
from core_mastery.task_store import Task, TaskNotFoundError, TaskStore, TaskStoreError


def test_missing_store_is_empty_without_creating_file(tmp_path):
    path = tmp_path / "tasks.json"
    assert TaskStore(path).list_tasks() == ()
    assert not path.exists()


def test_add_round_trip_and_ids(tmp_path):
    path = tmp_path / "tasks.json"
    first = TaskStore(path).add("  Study\tPython  ")
    second = TaskStore(path).add("Café practice")
    assert (first.id, first.title, first.completed) == (1, "Study Python", False)
    assert second.id == 2
    assert TaskStore(path).list_tasks() == (first, second)
    assert json.loads(path.read_text(encoding="utf-8"))["version"] == 1


def test_completion_persists_and_is_idempotent(tmp_path):
    path = tmp_path / "tasks.json"
    store = TaskStore(path)
    original = store.add("Practice")
    updated = store.complete(1)
    assert updated.completed and not original.completed
    before = path.read_bytes()
    assert TaskStore(path).complete(1) == updated
    assert path.read_bytes() == before
    assert TaskStore(path).list_tasks() == (updated,)


def test_returned_tasks_are_immutable():
    task = Task(1, "Practice")
    with pytest.raises(FrozenInstanceError):
        task.completed = True


@pytest.mark.parametrize("title", ["", " \t", "x" * 201, "bad\x1btitle", None])
def test_invalid_title_does_not_create_store(tmp_path, title):
    path = tmp_path / "tasks.json"
    with pytest.raises(ValueError):
        TaskStore(path).add(title)
    assert not path.exists()


def test_unknown_id_preserves_store(tmp_path):
    path = tmp_path / "tasks.json"
    store = TaskStore(path)
    store.add("Practice")
    before = path.read_bytes()
    with pytest.raises(TaskNotFoundError):
        store.complete(2)
    assert path.read_bytes() == before


@pytest.mark.parametrize("task_id", [0, -1, True, "1"])
def test_invalid_id(tmp_path, task_id):
    with pytest.raises(ValueError):
        TaskStore(tmp_path / "tasks.json").complete(task_id)


@pytest.mark.parametrize(
    "payload",
    [
        "",
        "{",
        "[]",
        '{"version": 2, "tasks": []}',
        '{"version": true, "tasks": []}',
        '{"version": 1, "tasks": null}',
        '{"version": 1, "tasks": [{}]}',
        '{"version": 1, "tasks": [{"id": true, "title": "X", "completed": false}]}',
        '{"version": 1, "tasks": [{"id": 1, "title": "X", "completed": "no"}]}',
    ],
)
def test_corrupt_store_not_overwritten(tmp_path, payload):
    path = tmp_path / "tasks.json"
    path.write_text(payload, encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(TaskStoreError):
        TaskStore(path).add("New task")
    assert path.read_bytes() == before


def test_duplicate_ids_rejected(tmp_path):
    path = tmp_path / "tasks.json"
    record = {"id": 1, "title": "X", "completed": False}
    path.write_text(json.dumps({"version": 1, "tasks": [record, record]}))
    with pytest.raises(TaskStoreError):
        TaskStore(path).list_tasks()


def test_invalid_utf8(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_bytes(b"\xff")
    with pytest.raises(TaskStoreError) as caught:
        TaskStore(path).list_tasks()
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_missing_parent_is_not_created(tmp_path):
    path = tmp_path / "missing" / "tasks.json"
    with pytest.raises(TaskStoreError):
        TaskStore(path).add("Practice")
    assert not path.parent.exists()


def test_replace_failure_preserves_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    store = TaskStore(path)
    store.add("Original")
    before = path.read_bytes()

    def denied(*args):
        raise PermissionError("denied")

    monkeypatch.setattr(context_managers.os, "replace", denied)
    with pytest.raises(TaskStoreError) as caught:
        store.add("New")
    assert isinstance(caught.value.__cause__, PermissionError)
    assert path.read_bytes() == before
    assert list(tmp_path.iterdir()) == [path]


def test_store_path_is_directory(tmp_path):
    with pytest.raises(TaskStoreError):
        TaskStore(tmp_path).list_tasks()
