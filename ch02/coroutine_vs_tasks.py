"""
Demo to show the execution of two long I/O co-routines
"""
import asyncio
from time import sleep, time


async def say_morning(sleep_sec: int) -> str:
    await asyncio.sleep(sleep_sec)
    return "Good morning"


async def say_goodnight(sleep_sec: int) -> str:
    print("Entering `say_goodnight`")
    await asyncio.sleep(sleep_sec)
    return "Good night"


async def main_coroutines():
    """
    This shows that the `await` pauses our current coroutine and won’t execute any other code
    inside that coroutine until the `await` expression gives us a value as a result
    Our code behaves as if it were sequential in this case
    """
    sec = 5
    start = time()
    print(await say_morning(sec))
    print(await say_goodnight(sec))
    print(f"Greetings coroutines ending at: {time() - start:.2f}")
    start = time()
    print(blocking_say_morning(sec))
    print(blocking_say_goodnight(sec))
    print(f"Greetings blocking ending at: {time() - start:.2f}")


async def main_tasks():
    """
    With tasks, we are able to run the concurrently,
    the first time we hit an `await` statement after creating a task, any tasks that are pending will run.
    the `await` triggers an iteration of the event loop.
    """
    sec = 5
    start = time()
    task_1 = asyncio.create_task(say_morning(sec))
    task_2 = asyncio.create_task(say_goodnight(sec))
    print(await task_1)
    print(await task_2)
    print(f"Greetings tasks ending at: {time() - start:.2f}")
    start = time()
    print(blocking_say_morning(sec))
    print(blocking_say_goodnight(sec))
    print(f"Greetings blocking ending at: {time() - start:.2f}")


def blocking_say_morning(sleep_sec: int) -> str:
    sleep(sleep_sec)
    return "Good morning"


def blocking_say_goodnight(sleep_sec: int) -> str:
    print("Entering `blocking_say_goodnight`")
    sleep(sleep_sec)
    return "Good night"


if __name__ == "__main__":
    asyncio.run(main_tasks())
    # asyncio.run(main_coroutines())
