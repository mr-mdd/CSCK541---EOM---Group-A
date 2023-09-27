"""Module for receiving data from client"""
from enum import Enum
from branston import Branston
from branston import Format, Source
import socket

# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 27/09/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php


class ServerDestination(Enum):
    Print = 16
    File = 32


class Server:
    PORT_NUMBER = 30687  # Port Number (# days of Saturn's Orbit, in case you were wondering)
    BACKLOG = 5  # Required for Listen
    BUFFER_SIZE = 1024
    FILE_NAME = "server_output.txt"

    def __init__(self):
        # Default to Printing
        self._destination = ServerDestination.Print
        # Default to Dictionary
        self._data_source = Source.Dictionary

        self.pickled_data = ""
        self.unpickled_data = None
        self.pickler = Branston()
        # Default to not encrypted
        self._encrypted = False

    def get_encrypted_flag(self):
        """Attribute Getter for whether data is encrypted"""
        return self._encrypted

    def set_encrypted_flag(self, encrypt):
        """Attribute Setter for whether data is encrypted"""
        self._encrypted = encrypt

    def set_destination(self, destination):
        """Attribute Setter for destination"""
        if destination in ServerDestination:
            self._destination = destination
        else:
            raise Exception("Invalid Server Destination")

    def set_source(self, source):
        """Attribute Setter for source"""
        self.pickler.set_source_type(source)

    def set_pickling_format(self, pickling_format):
        """Attribute Setter for the Pickling Format"""
        self.pickler.set_pickling_format(pickling_format)

    @staticmethod
    def get_server_host():
        """Returns the hostname of the server machine for passing to client"""
        return socket.gethostname()  # Local Machine Name

    def _get_socket(self):
        """Returns a socket"""
        host = socket.gethostname()  # Local Machine Name
        my_sock = socket.socket()  # Create a socket object
        port = self.PORT_NUMBER  # reserve a port
        my_sock.bind((host, port))  # bind the socket to the port of the machine
        return my_sock

    def listen(self):
        """Sets the socket listening for clients"""
        sock = self._get_socket()
        sock.listen(self.BACKLOG)  # wait for client connection

        while True:
            # Establish connection with client
            conn, addr = sock.accept()
            print("Got connection from", addr)

            # Receive data from client
            data = conn.recv(self.BUFFER_SIZE)
            print("Server received", repr(data))

            conn.send("Thank you for connecting")
            conn.close()

    def output(self):
        """Outputs the unpickled data"""
        if self._destination == ServerDestination.Print:
            print(self.unpickled_data)
        else:
            with open(self.FILE_NAME, "wb") as outfile:
                outfile.write(self.unpickled_data)

    def parse_settings(self, total):
        """Parses settings from client for Destination, data format, and encryption"""
        # Destination
        if total >= ServerDestination.File:
            self.set_destination(ServerDestination.File)
        else:
            self.set_destination(ServerDestination.Print)

        # Source Type
        total -= self._destination
        if total >= Source.TextFile:
            self.set_source(Source.TextFile)
        else:
            self.set_source(Source.Dictionary)

        # Format
        total -= self._data_source
        if total > 0:
            self.set_pickling_format(Format(total))
