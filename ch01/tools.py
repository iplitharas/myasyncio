from time import perf_counter_ns
from typing import Any, Callable


def time_it(fn: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        now = perf_counter_ns()
        print(f"Calling `{fn.__name__}` with {args}")
        result = fn(*args, **kwargs)
        end = perf_counter_ns() - now
        print(f"Total time: {end:.2f}")
        return result

    return inner
