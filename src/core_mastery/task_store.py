"""Validated tasks and a versioned JSON store for single-process CLI use."""

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from core_mastery.context_managers import staged_text_writer
from core_mastery.strings_and_files import normalize_whitespace


class TaskStoreError(Exception):
    """Expected task storage or data-format failure."""


class TaskNotFoundError(Exception):
    """The requested task ID is absent."""


@dataclass(frozen=True)
class Task:
    """Immutable task snapshot with a positive ID and canonical display title."""

    id: int
    title: str
    completed: bool = False

    def __post_init__(self) -> None:
        if type(self.id) is not int or self.id < 1:
            raise ValueError("task ID must be a positive integer")
        if (
            not isinstance(self.title, str)
            or not 1 <= len(self.title) <= 200
            or not self.title.isprintable()
            or normalize_whitespace(self.title) != self.title
        ):
            raise ValueError(
                "title must be 1-200 printable characters with clean spacing"
            )
        if type(self.completed) is not bool:
            raise ValueError("completed must be a boolean")


class TaskStore:
    """Read on every operation; publish writes using Day 6's staged writer.

    No locking: concurrent writers can overwrite each other's changes. Existing
    invalid data is never silently reset. A missing file represents an empty list.
    Parent directories must already exist. JSON is held in memory.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def list_tasks(self) -> tuple[Task, ...]:
        """Return validated immutable snapshots in stored order."""
        try:
            with self.path.open(encoding="utf-8") as stream:
                data = json.load(stream)
        except FileNotFoundError:
            return ()
        except OSError as error:
            raise TaskStoreError("Unable to read task file") from error
        except (ValueError, UnicodeError) as error:
            raise TaskStoreError("Task file is not valid UTF-8 JSON") from error
        try:
            if (
                not isinstance(data, dict)
                or set(data) != {"version", "tasks"}
                or type(data["version"]) is not int
                or data["version"] != 1
                or not isinstance(data["tasks"], list)
            ):
                raise ValueError("unsupported task format")
            tasks = []
            seen: set[int] = set()
            for record in data["tasks"]:
                if not isinstance(record, dict) or set(record) != {
                    "id",
                    "title",
                    "completed",
                }:
                    raise ValueError("invalid task record")
                task = Task(**record)
                if task.id in seen:
                    raise ValueError("duplicate task ID")
                seen.add(task.id)
                tasks.append(task)
            return tuple(tasks)
        except (TypeError, ValueError) as error:
            raise TaskStoreError(
                "Task file has an invalid or unsupported schema"
            ) from error

    def _save(self, tasks: tuple[Task, ...]) -> None:
        payload = {"version": 1, "tasks": [asdict(task) for task in tasks]}
        try:
            with staged_text_writer(self.path) as stream:
                json.dump(payload, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        except OSError as error:
            raise TaskStoreError("Unable to save task file") from error

    def add(self, title: str) -> Task:
        """Normalize whitespace, assign max existing ID + 1, and persist a task."""
        if not isinstance(title, str):
            raise ValueError("title must be a string")
        tasks = self.list_tasks()
        task = Task(
            max((task.id for task in tasks), default=0) + 1, normalize_whitespace(title)
        )
        self._save((*tasks, task))
        return task

    def complete(self, task_id: int) -> Task:
        """Mark a task complete; repeated completion is a no-write success."""
        if type(task_id) is not int or task_id < 1:
            raise ValueError("task ID must be a positive integer")
        tasks = self.list_tasks()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                if task.completed:
                    return task
                updated = replace(task, completed=True)
                self._save((*tasks[:index], updated, *tasks[index + 1 :]))
                return updated
        raise TaskNotFoundError(f"Task {task_id} not found")
