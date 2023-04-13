"""
Simple `GIL` released demo
"""
import threading
import requests

from ch01.tools import time_it


def simple_request() -> None:
    """Make a simple request"""
    response = requests.get("https://www.google.com")
    print(f"Response status code: {response.status_code}")


@time_it
def requests_no_threading() -> None:
    simple_request()
    simple_request()


@time_it
def requests_with_threading() -> None:
    thread_1 = threading.Thread(target=simple_request)
    thread_2 = threading.Thread(target=simple_request)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()


if __name__ == "__main__":
    requests_no_threading()
    requests_with_threading()
