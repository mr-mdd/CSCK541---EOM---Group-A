"""Module for sending data to server"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 27/09/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

from branston import Branston
from enum import Enum
from branston import Format
import socket


class Client:
    PORT_NUMBER = 30687  # Port Number (days of Saturn's Orbit)
    BACKLOG = 5  # Required for Listen
    BUFFER_SIZE = 1024

    def __init__(self):
        self.pickler = Branston()

    def _get_socket(self):
        host = socket.gethostname()  # Local Machine Name
        my_sock = socket.socket()  # Create a socket object
        port = self.PORT_NUMBER  # reserve a port
        my_sock.connect((host, port))  # bind the socket to the port of the machine
        return my_sock

    def connect(self):
        sock = self._get_socket()
        sock.send("Hello server")
