

## Sessions 

`aiohttp`, and web requests in general, employ the concept of a **session**.
Think of a session as opening a new **browser window**.
Within a new browser window, you’ll make connections to any number of web pages,
which may send you cookies that your browser saves for you.
With a session, you’ll keep many connections open, which can then be recycled.
This is known as connection pooling. `Connection pooling` is an important concept 
that aids the performance of our aiohttp-based applications.
Since creating connections is resource intensive,
creating a reusable pool of them cuts down on resource allocation costs. 
A session will also internally save any cookies that we receive, although this 
functionality can be turned off if desired.


## Setting timeouts
By default, aiohttp has a timeout of five minutes,
which means that no single operation should take longer than that.
> We can specify timeouts using the aiohttp-specific ClientTimeout data structure.
> This structure not only allows us to specify a total timeout in seconds 
> for an entire request but also allows us to set timeouts on 
> establishing a connection or reading data


## Running tasks concurrently, revisited
```python
import asyncio
 
 async def main() -> None:
    delay_times = [3, 3, 3]
    [await asyncio.create_task(asyncio.sleep(seconds)) for seconds in delay_times]
 
asyncio.run(main())
```
> Given that we ideally want the delay tasks to run concurrently,
> we’d expect the main method to complete in about 3 seconds.
> However, in this case 9 seconds elapse to run,
> since everything is done **sequentially**


The problem here is subtle. It occurs because we use `await` as soon as we create the 
task.
This means that we pause the list comprehension and the main coroutine
for every `delay` task we create until that `delay task` completes.
In this case, we will have only one task running at any given time,
instead of running multiple tasks concurrently.
The fix is easy, although a bit verbose.
We can create the tasks in one list comprehension and `await` in a second.
This lets everything to run concurrently.
```python
import asyncio
 
async def main() -> None:
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(asyncio.sleep(seconds)) for seconds in delay_times]
    [await task for task in tasks]
 
asyncio.run(main())
```

## Running tasks with gather
A widely used asyncio API functions for running `awaitables` concurrently is `asyncio.gather`.
This function takes in a sequence of `awaitables` and lets us run them concurrently,
all in one line of code. If any of the `awaitable`s we pass in is a **coroutine**,
gather **will automatically wrap it in a task to ensure that it runs concurrently**

> `asyncio.gather` returns an awaitable.
> When we use it in an `await` expression, it will pause until all `awaitables`
> that we passed into it are complete.
> Once everything we passed in finishes,`asyncio.gather` 
> will return a list of the completed results.