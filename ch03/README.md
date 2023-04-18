
<!-- TOC -->
  * [Working with blocking sockets](#working-with-blocking-sockets)
<!-- TOC -->

## Working with blocking sockets
> A socket is a way to read and write data over a network.
> We can think of a socket as a mailbox: we put a letter in,
> and it is delivered to the recipient’s address.
> The recipient can then read that message, and possibly send us another back.

The socket class has a method named `recv` that we can use to get data 
from a particular socket.
This method takes an integer representing the number of bytes we wish to read at a 
given time.
This is important because we can’t read all data from a socket at once;
we need to buffer until we reach the end of the input.


## Non blocking sockets
Fundamentally, creating a non-blocking socket is no different from creating a 
blocking one, except that we must call `setblocking` with `False`.
By default, a `socket` will have this value set to `True`, indicating it is blocking. 


## Build a socket event loop
> Operating systems have efficient APIs that let us watch sockets
> for incoming data and other events built in.
> While the actual API is dependent on the operating system (kqueue, epoll, 
> and IOCP are a few common ones),
> all of these I/O notification systems operate on a similar concept.
> We give them a list of sockets we want to monitor for events,
> and instead of constantly checking each socket
> to see if it has data, **the operating system tells us explicitly when sockets have data.**

These notification systems are the core of how asyncio achieves concurrency.
The event notification systems are different depending on the operating system.
Luckily, Python’s `selectors` module is abstracted such that we can get the 
proper event for wherever we run our code.
This makes our code portable across different operating systems.

In the asyncio event loop, when any of these two things happen,
coroutines that are waiting to run will do so until they either complete or
they hit the next `await` statement.
When we hit an `await` in a coroutine that utilizes a non-blocking socket
**it will register that socket with the system’s selector** and keep track that the 
coroutine is paused waiting for a result.
We can translate this into pseudocode that demonstrates the concept.
```
paused = []
ready = []
while True:
    paused, new_sockets = run_ready_tasks(ready)
    # register any new sockets
	selector.register(new_sockets)
	# set up the timeout
    timeout = calculate_timeout()
    events = selector.select(timeout)
    # process the events
    ready = process_events(events)
```
> We run any coroutines that are ready to run until they are paused on an `await` 
> statement and store those in the paused array.
> We also keep track of any new sockets we need to watch from running those 
> coroutines and register them with the selector.
> We then calculate the desired timeout for when we call `select`