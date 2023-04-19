"""
`asyncio.gather` allows us to run a lot of
"""

import asyncio

from aiohttp import ClientSession


async def fetch(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


async def main():
    async with ClientSession() as session:
        urls = [
            "https://google.com",
            "https://bbc.com",
            "http://python.org",
            "http://mywebsitet.org",
        ]
        requests = [fetch(session=session, url=url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)
        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [
            res for res in results if not isinstance(res, Exception)
        ]
        print(f"Exceptions: {exceptions}")
        print(f"Results: {successful_results}")


if __name__ == "__main__":
    asyncio.run(main())
