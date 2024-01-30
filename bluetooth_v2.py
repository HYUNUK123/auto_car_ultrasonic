# -*- coding: utf-8 -*-

from bluetooth import *

def setup_bluetooth():
    server_socket = BluetoothSocket(RFCOMM)

    port = PORT_ANY
    server_socket.bind(("", port))
    server_socket.listen(1)

    port = server_socket.getsockname()[1]
    print("Listening on port: %d" % port)

    client_socket, address = server_socket.accept()
    print("Accepted connection from ", address)

    client_socket.send(b"bluetooth connected!")

    return client_socket, server_socket

def recv_string(client_socket, server_socket):
    while True:
        data = client_socket.recv(32).decode('utf-8').strip()
        print("Received: %s" % data)
        return data
