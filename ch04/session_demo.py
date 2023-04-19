"""
`aiohttp` session demo
"""
import asyncio

import aiohttp
from aiohttp import ClientSession

from tools import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    """
    Perform a simple async http `GET` request
    """
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.google.com"
        status = await fetch_status(session=session, url=url)
        print(f"Status code from: {url} is: {status}")


if __name__ == "__main__":
    asyncio.run(main())
