"""
Once we create our server socket, we’ll register it with the default selector,
which will listen for any connections from clients.
Then, any time someone connects to our server socket,
we’ll register the client’s connection socket with the selector to watch for any data sent.
If we get any data from a socket that isn’t our server socket,
we know it is from a client that has sent data. We then receive that data and write it back to the client
"""
import selectors
import socket
from selectors import DefaultSelector


def create_web_server_socket(address: tuple = ("127.0.0.1", 8000)):
    selector = DefaultSelector()
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    print(f"Listening at: {address}")
    server_socket.listen()
    selector.register(server_socket, selectors.EVENT_READ)
    # Serve
    while True:
        events = selector.select(timeout=1)
        if len(events) == 0:
            print("No events yet,waiting a bit more!")
        for event, _ in events:
            event_socket = event.fileobj

            if event_socket == server_socket:
                # we have a new connection
                conn, address = server_socket.accept()
                conn.setblocking(False)
                # create a small buffer
                selector.register(conn, selectors.EVENT_READ)
            else:
                data = event_socket.recv(1024)
                print(f"I got some data: {data}")
                event_socket.send(b"server says:" + data)


if __name__ == "__main__":
    create_web_server_socket()
