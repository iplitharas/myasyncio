"""
Coroutine examples
"""
import asyncio


async def coroutine_hello_world():
    """
    Create a simple coroutine
    """
    print("Hello world")


def hello_world():
    print("Hello world")


if __name__ == "__main__":
    hello_world()
    coroutine = coroutine_hello_world()
    print(coroutine_hello_world())
    # To be able to run the coroutine we have to add it
    # in an event loop
    asyncio.run(coroutine_hello_world())
