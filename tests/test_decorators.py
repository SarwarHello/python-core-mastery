"""Deterministic decorator tests: no sleeps or wall-clock assertions."""

from inspect import signature

import pytest

from core_mastery.decorators import timed


def test_arguments_result_and_report_order():
    events = []
    ticks = iter([10.0, 10.25])

    def report(name, seconds):
        events.append((name, seconds))

    @timed(report, clock=lambda: next(ticks))
    def add(left: int, *, right: int = 1) -> int:
        events.append("called")
        return left + right

    assert add(3, right=4) == 7
    assert events == ["called", ("add", 0.25)]


def test_metadata_and_signature_preserved():
    def original(value: int, *, scale: int = 2) -> int:
        """Scale a value."""
        return value * scale

    decorated = timed(lambda *_: None, clock=lambda: 0.0)(original)
    assert decorated.__name__ == original.__name__
    assert decorated.__doc__ == original.__doc__
    assert decorated.__annotations__ == original.__annotations__
    assert decorated.__wrapped__ is original
    assert signature(decorated) == signature(original)


def test_original_return_object_preserved():
    result = []
    decorated = timed(lambda *_: None, clock=lambda: 0.0)(lambda: result)
    assert decorated() is result


def test_wrapped_exception_propagates_without_report():
    reports = []
    error = ValueError("failed")

    @timed(lambda *args: reports.append(args), clock=lambda: 0.0)
    def fail():
        raise error

    with pytest.raises(ValueError) as caught:
        fail()
    assert caught.value is error
    assert reports == []


def test_repeated_calls_have_separate_measurements():
    reports = []
    ticks = iter([1.0, 1.5, 4.0, 6.0])
    decorated = timed(lambda *args: reports.append(args), clock=lambda: next(ticks))(
        lambda: None
    )
    decorated()
    decorated()
    assert [seconds for _, seconds in reports] == [0.5, 2.0]


def test_decorated_instance_method():
    class Multiplier:
        @timed(lambda *_: None, clock=lambda: 0.0)
        def multiply(self, value):
            return value * 2

    assert Multiplier().multiply(3) == 6


def test_report_error_propagates_after_function_completes():
    called = []

    def report(*args):
        raise RuntimeError("report unavailable")

    @timed(report, clock=lambda: 0.0)
    def work():
        called.append(True)

    with pytest.raises(RuntimeError, match="report unavailable"):
        work()
    assert called == [True]


def test_initial_clock_error_prevents_execution():
    called = []

    def clock():
        raise RuntimeError("clock unavailable")

    decorated = timed(lambda *_: None, clock=clock)(lambda: called.append(True))
    with pytest.raises(RuntimeError, match="clock unavailable"):
        decorated()
    assert called == []


def test_generator_function_rejected():
    def generate():
        yield 1

    with pytest.raises(TypeError, match="synchronous"):
        timed(lambda *_: None)(generate)


def test_coroutine_function_rejected():
    async def work():
        return 1

    with pytest.raises(TypeError, match="synchronous"):
        timed(lambda *_: None)(work)


def test_async_generator_rejected():
    async def generate():
        yield 1

    with pytest.raises(TypeError, match="synchronous"):
        timed(lambda *_: None)(generate)
