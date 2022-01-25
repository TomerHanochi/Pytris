import functools
from time import perf_counter
from typing import Callable, Any


def cooldown(duration: float) -> Callable:
    def decorator(method: Callable) -> Callable:
        last_called = perf_counter()

        @functools.wraps(method)
        def wrapper(*args, **kwargs) -> Any:
            nonlocal last_called
            now = perf_counter()
            if now - last_called >= duration:
                last_called = now
                return method(*args, **kwargs)

        return wrapper

    return decorator
