"""
Future demo
"""
from asyncio import Future


def future_demo():
    my_future = Future()
    print(f"is my future done?{my_future.done()}")
    my_future.set_result(42)
    print(f"is my future done?{my_future.done()}")
    print(f"and what's the result: {my_future.result()}")


if __name__ == "__main__":
    future_demo()
