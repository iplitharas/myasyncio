import asyncio

from tools import async_timed, delay


@async_timed()
async def main():
    first_task = asyncio.create_task(delay(2))
    second_task = asyncio.create_task(delay(4))
    await first_task
    await second_task


@async_timed()
async def go_routine_main():
    """
    This will run in total 6secs
    """
    await delay(2)
    await delay(4)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(go_routine_main())
