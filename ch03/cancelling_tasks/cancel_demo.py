"""
The loop has a method
`add_signal_handler` where we can register our logic to specific unix signals
"""
import asyncio
import signal
from asyncio import AbstractEventLoop
from typing import Set

from tools import delay


def cancel_tasks() -> None:
    print("Got a `SIGINT`")
    all_tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f"Cancelling #{len(all_tasks)} task(s)")
    [task.cancel() for task in all_tasks]


async def main() -> None:
    """
    terminating tasks demo
    """
    loop: AbstractEventLoop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    task = asyncio.create_task(delay(10))
    await task


if __name__ == "__main__":
    asyncio.run(main())
