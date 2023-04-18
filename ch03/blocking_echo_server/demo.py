"""
The web server will listen to one `socket` and
for each client request will establish a new
`socket`
"""


import socket


def create_web_server_socket(address: tuple = ("127.0.0.1", 8000)):
    # SOCK_STREAM -> TCP
    # AF_INET -> hostname port
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # Allow us to reuse the port number after we stop and restart the application
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Set the address
    server_socket.bind(address)
    # Open the socket
    print(f"Listening at: {address}")
    server_socket.listen()
    # Serve
    try:
        connection, client_address = server_socket.accept()
        print(f"Got a connection from: {client_address}")
        # create a small buffer
        buffer = b""
        while buffer[-2:] != b"\r\n":
            # read 2 bytes
            data = connection.recv(2)
            if not data:
                break
            else:
                buffer += data
                print(f"got data: {data}")
        print(f"Client says: {buffer}")
        connection.sendall(b">>Server says: " + buffer)
    finally:
        print("Closing the connection")
        connection.close()


if __name__ == "__main__":
    create_web_server_socket()
