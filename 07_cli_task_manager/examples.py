"""Run the CLI in separate processes using disposable task storage."""

import subprocess
import sys
from tempfile import TemporaryDirectory


def main() -> None:
    """Demonstrate persistence without writing to the user's real task file."""
    with TemporaryDirectory() as directory:
        for arguments in (
            ["add", "Review Python basics"],
            ["add", "Write CLI tests"],
            ["list"],
            ["complete", "1"],
            ["list", "--status", "open"],
            ["list", "--status", "done"],
        ):
            result = subprocess.run(
                [sys.executable, "-m", "core_mastery.task_cli", *arguments],
                cwd=directory,
                text=True,
                capture_output=True,
                check=True,
                timeout=15,
            )
            print(result.stdout, end="")


if __name__ == "__main__":
    main()
