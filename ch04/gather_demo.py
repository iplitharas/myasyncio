"""
`asyncio.gather` allows us to run a lot of
co-routines concurrently without explicit create a task for each
co-routine.
"""

import asyncio
from aiohttp import ClientSession
from tools import async_timed


@async_timed()
async def fetch(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with ClientSession() as session:
        urls = ["https://google.com", "https://bbc.com", "http://python.org"]
        requests = [fetch(session=session, url=url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


@async_timed()
async def main_blocking():
    async with ClientSession() as session:
        urls = ["https://google.com", "https://bbc.com", "http://python.org"]
        status_codes = [await fetch(session=session, url=url) for url in urls]
        print(status_codes)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main_blocking())
