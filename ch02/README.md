<!-- TOC -->
  * [Coroutines](#coroutines)
  * [asyncio.run](#asynciorun)
  * [Tasks](#tasks)
  * [Cancelling tasks](#cancelling-tasks)
<!-- TOC -->
## Coroutines

Think of a coroutine like a regular Python function but with the superpower 
that it can pause its execution when it encounters an operation that could take a while to 
complete.
> When that long-running operation is complete, we can “wake up” our paused coroutine and 
> finish executing any other code in that coroutine. While a paused coroutine is waiting for the operation it paused for to finish,
> we can run other code.

This running of other code while waiting is what gives our application concurrency.
We can also run several time-consuming operations concurrently, which can give our applications big performance improvements.


## asyncio.run

`asyncio.run` is doing a few important things in this scenario.
First, it creates a **brand-new event**. Once it successfully does so,
it takes whichever coroutine we pass into it and runs it until it completes,
returning the result.
This function will also do some cleanup of anything that might be left running after
the main coroutine finishes.
Once everything has finished, it shuts down and closes the event loop.


## Tasks 

Tasks are **wrappers** around a **coroutine** that schedule a coroutine to run on the 
event loop as soon as possible.
This scheduling and execution happen in a **non-blocking fashion**,
meaning that, once we create a task,
we can execute other code instantly while the task is running.
> This contrasts with using the `await` keyword that acts in a **blocking** **manner**,
> meaning that we pause the entire coroutine until the result of the `await` expression comes 
> back.

Creating a task is achieved by using the `asyncio.create_task` function.
When we call this function, we give it a coroutine to run,
and it returns a task object instantly.
Once we have a task object, we can put it in an `await` expression that will extract the 
return value **once it is complete**


## Cancelling tasks
Something important to note about cancellation is that a `CancelledError` can only be thrown 
from an `await` statement.
This means that if we call cancel on a task when it is executing plain Python code,
that code will run until completion until we hit the next await statement (if one exists)
and a `CancelledError` can be raised.
Calling cancel won’t magically stop the task in its tracks;
it will only stop the task if you’re currently at an await point or its next `await` point.