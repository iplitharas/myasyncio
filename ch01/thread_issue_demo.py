"""
Simple demo to show that due to `GIL`
even if we have two threads we aren't able to speed up the calculation process
because only on python process can execute python byte code
"""
import threading

from ch01.tools import time_it


@time_it
def fib_with_no_threading(number: int) -> None:
    """
    Calculates the fibonacci number, number+1
    """
    fib(number)
    fib(number + 1)


@time_it
def fib_with_threading(number: int) -> None:
    """
    Spawns a thread for number, number+1
    """
    thread_1 = threading.Thread(target=fib, args=(number,))
    thread_2 = threading.Thread(target=fib, args=(number + 1,))
    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()


def fib(number: int) -> int:
    """
    Recursive fibonacci calculation.
    """
    if number <= 1:
        return 0
    elif number == 2:
        return 1
    else:
        return fib(number - 1) + fib(number - 2)


if __name__ == "__main__":
    n = 10
    fib_with_threading(n)
    fib_with_no_threading(n)
