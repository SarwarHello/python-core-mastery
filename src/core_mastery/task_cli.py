"""Command-line task manager: core-tasks or python -m core_mastery.task_cli."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from core_mastery.task_store import TaskNotFoundError, TaskStore, TaskStoreError


def main(argv: Sequence[str] | None = None) -> int:
    """Run one command; return 0 on success, 1 on operational/data failure.

    Argparse handles help (exit 0) and invalid usage (exit 2). Global options such
    as --file precede the subcommand. Never initialize storage during help/list.
    """
    parser = argparse.ArgumentParser(description="Manage tasks in a local JSON file.")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(".task-manager.json"),
        help="task storage path (default: .task-manager.json in current directory)",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="add a task with a quoted title")
    add.add_argument("title")
    listing = commands.add_parser("list", help="list tasks in creation order")
    listing.add_argument("--status", choices=["all", "open", "done"], default="all")
    complete = commands.add_parser("complete", help="mark an existing task complete")
    complete.add_argument("task_id", type=int)
    args = parser.parse_args(argv)
    store = TaskStore(args.file)
    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"Added task {task.id}: {task.title}")
        elif args.command == "complete":
            task = store.complete(args.task_id)
            print(f"Completed task {task.id}: {task.title}")
        else:
            tasks = [
                task
                for task in store.list_tasks()
                if args.status == "all" or task.completed == (args.status == "done")
            ]
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                marker = "x" if task.completed else " "
                print(f"[{marker}] {task.id}: {task.title}")
    except (TaskStoreError, TaskNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
