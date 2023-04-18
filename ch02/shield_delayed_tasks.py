"""
If we don't want to cancel the task
but just to inform the user that the tasks is delayed
we can use the `shield` keyword
"""

import asyncio

from tools import delay


async def main():
    slow_task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(slow_task), 5)
    except TimeoutError:
        print("Task took longer than five seconds, it will finish soon!")
        result = await slow_task
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
