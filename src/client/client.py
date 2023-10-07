"""Module for sending data to server"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

from src.util.branston import Branston
import socket
from src.util.enums import SecurityLevel, Source
from src.util.crypt import Crypt


class Client:
    BUFFER_SIZE = 1024
    ENCODING_FORMAT = 'utf-8'

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
        host = self.hostname
        my_sock = socket.socket()
        port = self.port_number
        my_sock.connect((host, port))
        return my_sock

    def connect(self):
        self.sock = self._get_socket()
        self.send_initialisation_message()
        data = self.sock.recv(self.BUFFER_SIZE)
        if not data:
            print("No response from the server.")
            return
        else:
            self.message = data
            self.parse_message()
        self.send_payload()

    def prepare_package(self):
        if self.source == Source.Dictionary:
            self.pickler = Branston()
            self.pickler.set_pickling_format(self.format.value)
            self._package_data = self.pickler.pickle(self.dictionary)
        elif self.source == Source.TextFile:
            with open(self.filepath, "r") as infile:
                text_data = infile.readlines()
            if self.security == SecurityLevel.Encrypted.value:
                self.crypt = Crypt.with_key(self._public_key)
                self._package_data = self.crypt.encrypt(text_data)
            else:
                self._package_data = text_data

    def parse_message(self):
        split_message = self.message.decode(self.ENCODING_FORMAT).split('\x00')
        self.parts = split_message[1:-1]

        if self.parts[0] != "ACK":
            print("Message does not conform to Branston protocol")
        else:
            key = self.parts[-1]
            if key != "NULL":
                self._public_key = key

    # Message Protocol 1: Initialisation Message
    def send_initialisation_message(self):
        message = f"\0{self.format.value}\0{self.source.value}\0{self.security.value}\0"
        self.sock.send(message.encode(self.ENCODING_FORMAT))

    # Message Protocol 3: Payload Message
    def send_payload(self):
        self.prepare_package()
        message = f"\0{self._package_data}\0END\0"
        self.sock.send(message.encode(self.ENCODING_FORMAT))
