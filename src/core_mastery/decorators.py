"""A typed decorator factory with an injectable clock and report callback."""

from collections.abc import Callable
from functools import wraps
from inspect import isasyncgenfunction, iscoroutinefunction, isgeneratorfunction
from time import perf_counter


def timed[**P, R](
    report: Callable[[str, float], None], *, clock: Callable[[], float] = perf_counter
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Report elapsed seconds after a synchronous function returns successfully.

    Preserve metadata, signature introspection and the original return object.
    Wrapped exceptions propagate unchanged without a report. Reporting/clock
    failures also propagate; the wrapped function may already have completed.
    Generator and async functions are rejected because timing their creation is
    not timing their execution. Callables must follow the annotated contracts.
    """

    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        if (
            isgeneratorfunction(function)
            or iscoroutinefunction(function)
            or isasyncgenfunction(function)
        ):
            raise TypeError("timed requires a synchronous, non-generator function")

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            started = clock()
            result = function(*args, **kwargs)
            elapsed = clock() - started
            report(function.__name__, elapsed)
            return result

        return wrapper

    return decorate
