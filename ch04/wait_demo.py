"""
Instead of gather we can use the `wait`
"""

import asyncio
import logging
from aiohttp import ClientSession
import aiohttp

from tools import async_timed


async def fetch(session: ClientSession, url: str, delay: int = 3) -> int:
    async with session.get(url) as result:
        print(f"Go to sleep for {delay} sec(s)")
        await asyncio.sleep(delay)
        return result.status


@async_timed()
async def main_all():
    async with aiohttp.ClientSession() as session:
        good_request = fetch(session, "https://python.org")
        bad_request = fetch(session, "python:/ /bad")

        fetchers = [asyncio.create_task(good_request), asyncio.create_task(bad_request)]

        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    " Request got an exception", exc_info=done_task.exception()
                )


@async_timed()
async def main_all():
    """
    Because we use the default behaviour of the `wait` we will need to wait
    until all task complete to see if we have any exception
    """
    async with aiohttp.ClientSession() as session:
        good_request = fetch(session, "https://python.org")
        bad_request = fetch(session, "python:/ /bad")

        fetchers = [asyncio.create_task(good_request), asyncio.create_task(bad_request)]

        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    " Request got an exception", exc_info=done_task.exception()
                )


@async_timed()
async def main_first_exception():
    """
    If we use the first_exception we can immediately see the exception and handle it
    """
    async with aiohttp.ClientSession() as session:
        good_request = fetch(session, "https://python.org")
        bad_request = fetch(session, "python:/ /bad")

        fetchers = [asyncio.create_task(bad_request), asyncio.create_task(good_request)]

        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    " Request got an exception", exc_info=done_task.exception()
                )


@async_timed()
async def main_first_complete():
    """
    If we use the first_complete we can immediately process the task in a deterministic
    way compared with a gather
    """
    async with aiohttp.ClientSession() as session:
        slow_request = fetch(session, "https://python.org", delay=10)
        fast_request = fetch(session, "https://python.org", delay=1)

        pending = [
            asyncio.create_task(slow_request),
            asyncio.create_task(fast_request),
        ]

        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            print(f"Done task count: {len(done)}")
            print(f"Pending task count: {len(pending)}")

            for done_task in done:
                print(await done_task)


if __name__ == "__main__":
    asyncio.run(main_first_complete())
