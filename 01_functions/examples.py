"""Run: python 01_functions/examples.py after editable installation."""

from core_mastery.functions_lab import calculate_total, transform_values


def main() -> None:
    """Show a default, keyword-only option and typed callable."""
    print(calculate_total(250))
    print(calculate_total(250, 3, discount_percent=10))
    print(transform_values([1, 2, 3], str))


if __name__ == "__main__":
    main()
