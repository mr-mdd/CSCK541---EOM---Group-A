"""Module for sending data to server"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

from branston import Branston
import socket
from enums import SecurityLevel, Source
from crypt import Crypt


class Client:
    BUFFER_SIZE = 1024

    def __init__(self, settings):
        self.hostname = settings.hostname
        self.port_number = settings.port_number
        self.source = settings.source
        self.format = settings.data_format
        self.dictionary = settings.dictionary
        self.filepath = settings.filepath
        self.security = settings.security_level
        self.sock = None
        self.crypt = None
        self._public_key = None
        self.pickler = None
        self._package_data = None
        self.message = None
        self.parts = None

    def _get_socket(self):
        host = socket.gethostname()  # Local Machine Name
        my_sock = socket.socket()  # Create a socket object
        port = self.port_number  # reserve a port
        my_sock.connect((host, port))  # bind the socket to the port of the machine
        return my_sock

    def connect(self):
        sock = self._get_socket()
        self.sock = sock
        self.send_initialisation_message()

        while True:
            data = self.sock.recv(self.BUFFER_SIZE)
            if not data:
                continue
            else:
                self.message = data
                print(self.message)
                # Parse message for Public Key
                self.parse_message()
                # DoTheThang
                self.send_payload()

    def prepare_package(self):
        if self.source == Source.Dictionary:
            # pickle the data
            self.pickler = Branston()
            self.pickler.set_pickling_format(self.format)
            self._package_data = self.pickler.pickle(self.dictionary)

        if self.source == Source.TextFile:
            with open(self.filepath, "r") as infile:
                text_data = infile.readlines()
            if self.security == SecurityLevel.Encrypted:
                self.crypt = Crypt.with_key(self._public_key)
                self._package_data = self.crypt.encrypt(text_data)
            else:
                self._package_data = text_data

    def parse_message(self):
        self.parts = self.message.split('\0')
        # Message Protocol 2.1: Acknowledge message with Public Key
        # Message Protocol 2.2: Acknowledge message without Public Key
        if self.parts[0] != "ACK":
            # Spurious Message
            print("Message does not conform to Branston protocol")

        # Set Public Key
        key = self.parts[1]
        if key is not None:
            self._public_key = self.parts[1]

    # Message Protocol 1: Initialisation Message
    def send_initialisation_message(self):
        message = f"\0[{self.format}]\0[{self.source}]\0[{self.security}]\0"
        self.sock.send(message)

    # Message Protocol 3: Payload Message
    def send_payload(self):
        self.prepare_package()
        message = f"\0[{self._package_data}]\0END\0"
        self.sock.send(message)
