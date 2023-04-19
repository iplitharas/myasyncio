"""
`aiohttp` timeout demo.
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
    tens_mill = aiohttp.ClientTimeout(total=0.2)
    async with session.get(url, timeout=tens_mill) as result:
        return result.status


@async_timed()
async def main():
    session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = "https://www.google.com"
        status = await fetch_status(session=session, url=url)
        print(f"Status code from: {url} is: {status}")


if __name__ == "__main__":
    asyncio.run(main())
