<!-- TOC -->
  * [Concurrency](#concurrency)
  * [Parallelism](#parallelism)
  * [The difference between concurrency and parallelism](#the-difference-between-concurrency-and-parallelism)
  * [Process](#process)
  * [Thread](#thread)
  * [Understanding the `global interpreter lock`](#understanding-the-global-interpreter-lock)
  * [How event-loop works](#how-event-loop-works)
<!-- TOC -->
## Concurrency
When we say two tasks are happening **concurrently**,
we mean those tasks are happening at the same time.
Take, for instance, a baker baking two different cakes.
To bake these cakes, we need to preheat our oven.
Preheating can take tens of minutes depending on the oven 
and the baking temperature,
but we don’t need to wait for our oven to preheat
before starting other tasks,
such as mixing the flour and sugar together with eggs.
We can do other work until the oven beeps, letting us know it is preheated.

> This switching between tasks (doing something else while the oven heats, switching between two different cakes) is 
> **concurrent behavior**.

## Parallelism
While `concurrency` implies that multiple tasks are in process simultaneously,
it does not imply that they are running together in parallel.
When we say something is running in parallel, we mean not only are there two or more tasks
happening concurrently, but they are also **executing at the same time**
> In a system that is only **concurrent**, we can switch between running these applications,
> running one application for a short while before letting the other one run.
> If we do this fast enough, it gives the appearance of two things happening at once.
> In a system that is **parallel**, two applications are running simultaneously,
> and we’re actively running two things concurrently.


## The difference between concurrency and parallelism
`Concurrency` is about multiple tasks that can happen independently from one another.
We can have concurrency on a CPU with only one core, as the operation will employ
preemptive multitasking to switch between tasks.
Parallelism, however, means that we must be executing two or more tasks at the same time.
On a machine with one core, this is not possible.
To make this possible, we need a CPU with multiple cores that can run two tasks together.

> While **parallelism** implies **concurrency**,
> concurrency does not always imply parallelism**.
> A multithreading application running on a multiple-core machine is both concurrent and parallel.
> In this setup, we have multiple tasks running at the same time,
> and there are two cores independently executing the code associated with those tasks.
> However, with **multitasking** we can have multiple tasks happening concurrently,
> yet only one of them is executing at a given time.


## Process
A `process` is an application run that has a memory space that other applications cannot access.
An example of creating a Python process would be running a simple “hello world” application 
or typing `python` at the command line to start up the REPL (read eval print loop).
Multiple processes can run on a single machine.
If we are on a machine that has a CPU with multiple cores,
we can execute multiple processes at the same time.
If we are on a CPU with only one core, we can still have multiple applications running simultaneously,
through time slicing.
When an operating system uses time slicing,
it will switch between which process is running automatically after some amount of time.
> The algorithms that determine when this switching occurs are different,
> depending on the operating system.


## Thread
Threads can be thought of as lighter-weight processes.
In addition, they are the smallest construct that can be managed by an operating system.
They do not have their own memory as does a process; instead, they share the memory of the process 
that created them. 
>Threads are associated with the process that created them
>A process will always have at least one thread associated with it, usually known as the `main thread`.
>A process can also create other threads, which are more commonly known as worker or background threads.

These threads can perform other work concurrently alongside the main thread.
Threads, much like processes, can run alongside one another on a multicore CPU,
and the operating system can also switch between them via time slicing.
When we run a normal Python application, we create a process as well as a main thread that will 
be responsible for running our Python application.

## Understanding the `global interpreter lock`
The `global interpreter lock`, abbreviated GIL and pronounced `gill`,
is a controversial topic in the Python community.
>Briefly, the GIL prevents one Python process from executing more than one Python bytecode 
>instruction at any given time.

This means that even **if we have multiple threads on a machine with multiple cores,
a Python process can have only one thread running Python code at a time**.
In a world where we have CPUs with multiple cores,
this can pose a significant challenge for Python developers looking to take advantage of 
multithreading to improve the performance of their application.

>Multiprocessing can run multiple bytecode instructions concurrently because each Python process has its own GIL.


>The global interpreter lock is released when I/O operations happen.
> This lets us employ threads to do concurrent work when it comes to I/O,
> but not for CPU-bound Python code itself

This model gives us concurrency but not parallelism.
In other languages, such as Java or C++, we would get true parallelism on multicore 
machines because we don’t have the GIL and can execute simultaneously.
However, in Python, because of the GIL, **the best we can do is concurrency of** 
our I/O operations, and only one piece of Python code is executing at a given time.


## How event-loop works
 The most basic event loop is extremely simple. We create a queue that holds a list of events or messages. We then loop forever, processing messages one at a time as they come into the queue.
 In Python, a basic event loop might look something like this
 ```python
from collections import deque
 
messages = deque()

def process_message(msg):
    pass 

while True:
    if messages:
        message = messages.pop()
        process_message(message)
 ```
In asyncio, the event loop keeps a queue of **tasks** instead of messages.
**Tasks** are **wrappers** around a **coroutine**.

> A coroutine can pause execution when it hits an I/O-bound operation 
> and will let the event loop run other tasks that are not waiting for I/O 
> operations to complete.

When we create an event loop, we create an empty queue of tasks.
We can then add tasks into the queue to be run.
Each iteration of the event loop checks for tasks that need to be run and will run them 
one at a time until a task hits an I/O operation.
At that time the task will be “paused,” and we instruct our operating system to 
watch any sockets for I/O to complete.
We then look for the next task to be run.
On every iteration of the event loop, we’ll check to see if any of our I/O has completed;
if it has, we’ll “wake up” any tasks that were paused and let them finish running