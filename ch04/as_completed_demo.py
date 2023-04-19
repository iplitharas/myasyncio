"""
With `asyncio.gather` we have to wait until all the tasks complete.
but with `as_completed` we can use the results
"""

import asyncio

from aiohttp import ClientSession


async def fetch(session: ClientSession, url: str, sleep: int) -> int:
    print(f"Go to sleep before fetching the: {url} for {sleep}")
    await asyncio.sleep(sleep)
    async with session.get(url) as result:
        return result.status


async def main():
    """
    Run the tasks and print their status as complete
    """
    async with ClientSession() as session:
        tasks = [
            fetch(session=session, url="http://www.python.org", sleep=1),
            fetch(session=session, url="http://www.python.org", sleep=10),
            fetch(session=session, url="http://www.python.org", sleep=15),
        ]
        for done_task in asyncio.as_completed(tasks, timeout=11):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print("We got a timeout error:")

        for task in asyncio.tasks.all_tasks():
            print(task)


if __name__ == "__main__":
    asyncio.run(main())
