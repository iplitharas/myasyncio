<!-- TOC -->
  * [Sessions](#sessions)
  * [Setting timeouts](#setting-timeouts)
  * [Running tasks concurrently, revisited](#running-tasks-concurrently-revisited)
  * [Running tasks with gather](#running-tasks-with-gather)
  * [Handling exceptions with gather](#handling-exceptions-with-gather)
  * [Processing requests as they complete](#processing-requests-as-they-complete)
  * [Finer-grained control with wait](#finer-grained-control-with-wait)
    * [Why wrap everything in a task](#why-wrap-everything-in-a-task)
<!-- TOC -->

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

It is worth noting that the results for each awaitable we pass in may not complete
in a deterministic order.
For example, if we pass coroutines `a` and `b` to `gather` in that order,
 `b` may complete before `a`

## Handling exceptions with gather
`asyncio.gather` gives us an optional parameter,`return_exceptions`,
which allows us to specify how we want to deal with exceptions from our `awaitables`.
 `return_exceptions`is a Boolean value; therefore,
it has two behaviors that we can choose from
1. `return_exceptions = False` 
This is the default value for `gather`.
In this case, if any of our coroutines throws an exception, our `gather`call will 
also throw that exception when we await it.
However, even though one of our coroutines failed, 
our other coroutines **are not canceled and will continue to run as long** 
as we handle the exception, or the exception does not result in the event 
loop stopping and canceling the tasks
2. `return_exceptions=True` In this case, `gather` will return any exceptions
as part of the result list it returns when we `await` it.
The call to `gather` will not throw any exceptions itself,
and we’ll be able handle all exceptions as we wish.


## Processing requests as they complete
While `asyncio.gather` will work for many cases,
it has the drawback that it waits for all `awaitables` to finish before
allowing access to any results.
This is a problem if we’d like to process results as soon as they come in.
It can also be a problem if we have a few `awaitables` that could complete 
quickly and a few which could take some time, since `gather` waits for everything
to finish.
This can cause our application to become unresponsive;
imagine a user makes 100 requests and two of them are slow,
but the rest complete quickly.
It would be great if once requests start to finish,
we could output some information to our users.

`as_completed` works well for getting results as fast as possible
but **has drawbacks**.
The first is that while we get results as they come in,
there isn’t any way to easily see which coroutine or task we’re awaiting
as the order is completely **nondeterministic**.
If we don’t care about order, this may be fine,
but if we need to associate the results to the requests somehow,
we’re left with a challenge.

The second is that with timeouts,
while we will correctly throw an exception and move on,
any tasks created will still be running in the background.
Since it’s hard to figure out which tasks are still running 
if we want to cancel them, we have another challenge

## Finer-grained control with wait
One of the drawbacks of both `gather` and `as_completed` is that
there is no easy way to cancel tasks that were already running
when we saw an exception.
This might be okay in many situations,
but imagine a use case in which we make several coroutine calls 
**and if the first one fails, the rest will as well**.
An example of this would be passing in an invalid parameter
to a web request or reaching an API rate limit.
This has the potential to cause performance issues because
we’ll consume more resources by having more tasks than we need.
Another drawback we noted with `as_completed`
is that, as the iteration order is nondeterministic,
it is challenging to keep track of exactly which task had completed.

`wait` in asyncio is similar to `gather`. `wait` 
that offers more specific control to handle these situations.
This method has several options to choose from depending on when we want our results.
In addition, this method returns two sets:
a set of tasks that are finished with either a result or an exception,
and a set of tasks that are still running. 
This function also allows us to specify a timeout that behaves differently
from how other API methods operate; it does not throw exceptions.
When needed, this function can solve some of the issues we noted with the 
other asyncio API functions we’ve used so far.

The basic signature of `wait`is a list of **awaitable** **objects**,
followed by an optional timeout and an optional `return_when` string.
This string has a few predefined values that we’ll examine:
`ALL_COMPLETED`,
`FIRST_EXCEPTION`
and `FIRST_COMPLETED`.
It defaults to `ALL_COMPLETED`.
While as of this writing,`wait` τakes a list of **awaitables**,
it will change in future versions of Python to only accept `task` objects.
We’ll see why at the end of this section,
but for these code samples, as this is best practice,
we’ll wrap all coroutines in tasks.


### Why wrap everything in a task
```python
import asyncio
import aiohttp
 
 async def main():
    async with aiohttp.ClientSession() as session:
        api_a = fetch_status(session, 'https:/ / www .example .com')
        api_b = fetch_status(session, 'https:/ / www .example .com', delay=2)
 
        done, pending = await asyncio.wait([api_a, api_b], timeout=1)
 
        for task in pending:
            if task is api_b:
                print('API B too slow, cancelling')
                task.cancel()
 
asyncio.run(main())
```
This can happen because when we call `wait` with just coroutines
they are automatically wrapped in tasks, and the `done`and `pending` 
sets returned are those **tasks** that`wait`created for us.
This means that we can’t do any comparisons to see which specific task is in the
`pending` set such as if task is api_b, since we’ll be comparing a task
object, we have no access to with a coroutine.
However, if we wrap fetch_status
in a task,wait won’t create any new objects,
and the comparison if task is api_b will work as we expect.
In this case, we’re correctly comparing two task objects.