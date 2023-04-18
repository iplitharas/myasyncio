
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