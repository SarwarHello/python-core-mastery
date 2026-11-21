"""CLI outputs, exit codes and persistence across real subprocesses."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from core_mastery.task_cli import main


def test_add_list_complete_workflow(tmp_path, capsys):
    args = ["--file", str(tmp_path / "tasks.json")]
    assert main([*args, "add", "Learn Python"]) == 0
    assert capsys.readouterr().out == "Added task 1: Learn Python\n"
    assert main([*args, "list"]) == 0
    assert capsys.readouterr().out == "[ ] 1: Learn Python\n"
    assert main([*args, "complete", "1"]) == 0
    assert capsys.readouterr().out == "Completed task 1: Learn Python\n"
    assert main([*args, "list", "--status", "done"]) == 0
    assert capsys.readouterr().out == "[x] 1: Learn Python\n"
    assert main([*args, "list", "--status", "open"]) == 0
    assert capsys.readouterr().out == "No tasks found.\n"


def test_empty_list_does_not_create_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["list"]) == 0
    assert capsys.readouterr().out == "No tasks found.\n"
    assert list(tmp_path.iterdir()) == []


def test_default_path_and_normalized_title(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["add", "  Read   docs "]) == 0
    assert (tmp_path / ".task-manager.json").exists()
    assert capsys.readouterr().out == "Added task 1: Read docs\n"


@pytest.mark.parametrize(
    "command", [["add", " "], ["complete", "0"], ["complete", "999"]]
)
def test_domain_error_is_stderr_and_no_write(tmp_path, capsys, command):
    path = tmp_path / "tasks.json"
    assert main(["--file", str(path), *command]) == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err.startswith("Error: ")
    assert "Traceback" not in output.err
    assert not path.exists()


@pytest.mark.parametrize(
    "args",
    [[], ["unknown"], ["add"], ["complete", "abc"], ["list", "--status", "wrong"]],
)
def test_usage_errors_exit_two(args):
    with pytest.raises(SystemExit) as caught:
        main(args)
    assert caught.value.code == 2


@pytest.mark.parametrize(
    "args", [["--help"], ["add", "--help"], ["list", "--help"], ["complete", "--help"]]
)
def test_help_does_not_touch_storage(tmp_path, monkeypatch, args):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as caught:
        main(args)
    assert caught.value.code == 0
    assert list(tmp_path.iterdir()) == []


def test_corrupt_store_reports_error_and_preserves_bytes(tmp_path, capsys):
    path = tmp_path / "tasks.json"
    path.write_bytes(b"broken")
    assert main(["--file", str(path), "add", "New"]) == 1
    output = capsys.readouterr()
    assert "Error:" in output.err and not output.out
    assert path.read_bytes() == b"broken"


def test_missing_parent_reports_error(tmp_path, capsys):
    path = tmp_path / "missing" / "tasks.json"
    assert main(["--file", str(path), "add", "New"]) == 1
    assert "Unable to save" in capsys.readouterr().err
    assert not path.parent.exists()


def test_real_subprocesses_share_persistent_store(tmp_path):
    base = [sys.executable, "-m", "core_mastery.task_cli", "--file", "tasks.json"]
    for args, expected in [
        (["add", "Separate process"], "Added task 1: Separate process"),
        (["complete", "1"], "Completed task 1: Separate process"),
        (["list"], "[x] 1: Separate process"),
    ]:
        result = subprocess.run(
            [*base, *args], cwd=tmp_path, text=True, capture_output=True, timeout=15
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == expected
        assert result.stderr == ""


def test_installed_console_entry_point(tmp_path):
    name = "core-tasks.exe" if os.name == "nt" else "core-tasks"
    executable = Path(sys.executable).parent / name
    result = subprocess.run(
        [str(executable), "list"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "No tasks found.\n"
    assert not list(tmp_path.iterdir())
