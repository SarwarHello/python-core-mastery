"""Run from the repository root after installing the package."""

from core_mastery import ordered_unique, word_frequencies


def main() -> None:
    """Print two deterministic collections examples."""
    print(ordered_unique(["Python", "SQL", "Python", "Git", "SQL"]))
    print(word_frequencies("Python, python! SQL and Python."))


if __name__ == "__main__":
    main()
