"""Module for sending data to server"""
import json

from rsa import PublicKey

# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

from src.util.branston import Branston
import socket
from src.util.enums import SecurityLevel, Source
from src.util.crypt import Crypt


class Client:
    BUFFER_SIZE = 1024  # 1KB
    ENCODING_FORMAT = 'utf-8'
    BYTE_ORDER = 'big'

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
        try:
            data = self.sock.recv(self.BUFFER_SIZE)

            if not data:
                print("No response from the server.")
                return
            else:
                self.message = data
                self.parse_message()
            self.send_payload()

        except OverflowError:
            print("Payload message is too big.")

    def prepare_package(self):
        if self.source == Source.Dictionary:
            self.pickler = Branston()
            self.pickler.set_pickling_format(self.format.value)
            package_data = self.pickler.pickle(self.dictionary)

            # Ensure the package data is in bytes
            if isinstance(package_data, str):
                package_data = package_data.encode(self.ENCODING_FORMAT).strip()

            self._package_data = package_data

        elif self.source == Source.TextFile:
            with open(self.filepath, "r") as infile:
                text_data = infile.read()
            if self.security == SecurityLevel.Encrypted:
                self.crypt = Crypt.with_key(self._public_key)
                encrypted_data = self.crypt.encrypt(text_data)

                # Ensure the encrypted data is in bytes
                if isinstance(encrypted_data, str):
                    encrypted_data = encrypted_data.encode(self.ENCODING_FORMAT).strip()

                self._package_data = encrypted_data
            else:
                self._package_data = text_data.encode(self.ENCODING_FORMAT)  # Convert to bytes

    def parse_message(self):
        # Skip Header (message_length) and decode the payload
        decoded_message = self.message[4:].decode(self.ENCODING_FORMAT)

        # Check message format
        if "ACK" in decoded_message and "END" in decoded_message:
            content_start = decoded_message.index("ACK") + 3  # +3 to skip "ACK"
            content_end = decoded_message.index("END")
            content = decoded_message[content_start:content_end].strip()

            if content == "NULL":
                self._public_key = None

            else:
                try:
                    key_data = json.loads(content)  # Directly load JSON from the content

                    if 'modulus' in key_data and 'exponent' in key_data:  # Built directly to avoid data corruption
                        modulus = int(key_data['modulus'])
                        exponent = int(key_data['exponent'])
                        self._public_key = PublicKey(modulus, exponent)
                    else:
                        print("Unexpected content format")

                except json.JSONDecodeError:
                    print("Failed to decode JSON content.")
        else:
            print("Message does not conform to Branston protocol")

    def send_initialisation_message(self):
        if self.format is None:
            format_byte = b'\x00'
        else:
            format_byte = self.format.value.to_bytes(1, self.BYTE_ORDER)

        message = format_byte + self.source.value.to_bytes(1, self.BYTE_ORDER) + self.security.value.to_bytes(1,
                                                                                                              self.BYTE_ORDER)

        length = len(message)
        self.sock.send(length.to_bytes(4, self.BYTE_ORDER) + message)

    def send_payload(self):
        self.prepare_package()
        end_marker = b"END"

        # Check if package_data is a string and convert it to bytes if so
        if isinstance(self._package_data, str):
            self._package_data = self._package_data.encode(self.ENCODING_FORMAT).strip()

        message_bytes = self._package_data + end_marker

        length = len(message_bytes)
        self.sock.send(length.to_bytes(4, self.BYTE_ORDER) + message_bytes)
