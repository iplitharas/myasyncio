"""
Instead of checking the time passed in the previous
example: `canceling_task_demo.py`
we can use the `wait_for` keyowrd
"""
import asyncio

from tools import delay


async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("got a timeout")
        print(f"was the task cancelled? {delay_task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
