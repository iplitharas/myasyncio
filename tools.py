"""Simple delay demo coroutine"""
import asyncio
import time
from functools import wraps
from typing import Callable


async def delay(delay_seconds: int) -> int:
    print(f"`delay`: sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"`delay`: finished sleeping for {delay_seconds} second(s)")
    return delay_seconds


def async_timed():
    def outer(func: Callable) -> Callable:
        @wraps(func)
        async def inner(*args, **kwargs) -> Callable:
            print(f"Starting func with: {args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"Finished {func} in total {total:.4f} second(s)")

        return inner

    return outer
