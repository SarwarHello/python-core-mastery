"""Run: python 02_data_structures/examples.py after editable installation."""

from core_mastery.data_structures import (
    compare_skills,
    group_members,
    score_bounds,
    top_scores,
)


def main() -> None:
    """Print deterministic examples of all four collection types."""
    print(top_scores([7, 9, 7, 2], limit=2))
    print(score_bounds(iter([7, 9, 2])))
    matched, missing = compare_skills({"Python", "SQL"}, {"Python", "Git"})
    print(sorted(matched), sorted(missing))
    print(group_members([("backend", "Ada"), ("data", "Lin"), ("backend", "Sam")]))


if __name__ == "__main__":
    main()
