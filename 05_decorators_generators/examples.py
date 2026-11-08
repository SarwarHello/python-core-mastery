"""Integrated example with an illustrative clock, not a real benchmark."""

from core_mastery.decorators import timed
from core_mastery.generators import batches, running_totals


def main() -> None:
    """Time consumption rather than creation of a lazy pipeline."""
    ticks = iter([10.0, 10.25])
    reports: list[tuple[str, float]] = []

    @timed(
        lambda name, seconds: reports.append((name, seconds)), clock=lambda: next(ticks)
    )
    def consume() -> list[tuple[int, ...]]:
        return list(batches(running_totals([2, 3, 4, 1]), 3))

    print(consume())
    name, seconds = reports[0]
    print(f"{name}: {seconds:.2f}s (illustrative clock)")
    stream = running_totals([1, 2, 3])
    print(f"First total: {next(stream)}")
    print(f"Remaining totals: {list(stream)}")
    print(f"Exhausted: {list(stream)}")


if __name__ == "__main__":
    main()
