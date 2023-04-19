"""
We can have as well async generators
"""
import asyncio


async def generator_demo(until: int = 10):
    for number in range(1, until):
        await asyncio.sleep(1)
        yield number


async def main():
    async_generator = generator_demo(20)
    print(f"type of the generator is: {async_generator}")
    async for number in async_generator:
        print(f"Got number: {number}")


if __name__ == "__main__":
    asyncio.run(main())
