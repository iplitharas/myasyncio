"""
Canceling a task demo
"""
import asyncio
from asyncio import CancelledError

from tools import delay


async def main():
    long_running_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0                                             
    while not long_running_task.done():
        print("Task not finished, check again in 1 sec")
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_running_task.cancel()

    try:
        # await the task to catch the exception
        await long_running_task
    except CancelledError:
        print(f"Task cancelled: {long_running_task.cancelled()} ")


if __name__ == "__main__":
    asyncio.run(main())
