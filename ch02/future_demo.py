"""
Future can be used in await statements
"""

import asyncio
from asyncio import Future


def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_feature_value(future=future))
    return future


async def set_feature_value(future: Future) -> None:
    await asyncio.sleep(delay=1)
    future.set_result(42)


async def main():
    future = make_request()
    print(f"Is the future done?: {future.done()}")
    value = await future
    print(f"Is the future done?: {future.done()}")
    print(value)


if __name__ == "__main__":
    asyncio.run(main())
