"""
The web server will listen to one `socket` and
for each client request will establish a new
`socket`
"""


import socket


def create_web_server_socket(address: tuple = ("127.0.0.1", 8000)):
    # SOCK_STREAM -> TCP
    # AF_INET -> hostname port
    server_socket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM
    )
    # Allow us to reuse the port number after we stop and restart the application
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Set the address
    server_socket.bind(address)
    # Open the socket
    print(f"Listening at: {address}")
    server_socket.listen()
    connections = []
    # Serve
    try:
        while True:
            # for each client create a new connection!
            # this will block the loop until we have a new connection
            # as a result, all the clients will have to wait
            connection, client_address = server_socket.accept()
            print(f"Got a connection from: {client_address}")
            connections.append(connection)
            for client_conn in connections:
                print(f"Total connections are: {len(connections)}")
                # create a small buffer
                buffer = b""
                while buffer[-2:] != b"\r\n":
                    # read 2 bytes
                    data = client_conn.recv(2)
                    print(f"I got data: {data}")
                    if not data:
                        break
                    else:
                        buffer += data

                print(f"Client says: {buffer}")
                client_conn.send(b">>Server says: " + buffer)
    finally:
        print("Closing the web-socket")
        server_socket.close()


if __name__ == "__main__":
    create_web_server_socket()
