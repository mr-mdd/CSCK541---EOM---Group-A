"""Module for sending data to server"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 28/09/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

from branston import Branston
import socket
from enums import *
from crypt import Crypt


class Client:
    PORT_NUMBER = 30687  # Port Number (days of Saturn's Orbit)
    BACKLOG = 5  # Required for Listen
    BUFFER_SIZE = 1024

    def __init__(self):
        self.pickler = Branston()
        self._pickled_data = None
        self._unpickled_data = None
        self.sock = None
        self.crypt = None
        self._public_key = None

    def _get_socket(self):
        host = socket.gethostname()  # Local Machine Name
        my_sock = socket.socket()  # Create a socket object
        port = self.PORT_NUMBER  # reserve a port
        my_sock.connect((host, port))  # bind the socket to the port of the machine
        return my_sock

    def connect(self):
        sock = self._get_socket()
        self.sock = sock
        self.sock.send(Conversation.CanISendData)

        while True:
            data = self.sock.recv(self.BUFFER_SIZE)
            if not data:
                continue
            else:
                # Filter data for message or content
                data = self.filter_data(data)
                print(data)

    def filter_data(self, message):
        """Is the incoming data a message or data?"""

        # Is this a message? If so perform action
        if message in Conversation:
            match message:
                case Conversation.CanISendData:
                    pass  # Server Side Only
                case Conversation.SendDataFormat:
                    combined_format = SecurityLevel.UnEncrypted.value + Source.Dictionary.value + Format.BINARY.value
                    self.send_data_format(combined_format)
                case Conversation.PublicKeyReceived:
                    pass  # Server Side Only
                case Conversation.SendData:
                    if self.pickler.get_encrypted_flag:
                        self.crypt = Crypt.client(self._public_key)
                        encrypted_data = self.crypt.encrypt(self._pickled_data)
                        self.sock.send(encrypted_data)
                    else:
                        self.sock.send(self._pickled_data)
                case Conversation.DataReceived:
                    self.sock.close()
            return None

        # If not a message then this is data
        else:
            return message

    def send_data_format(self, combined_value):
        self.sock.send(combined_value)

    def confirm_public_key_received(self):
        self.sock.send(Conversation.PublicKeyReceived)

    def send_data(self, data):
        self.sock.send(data)
