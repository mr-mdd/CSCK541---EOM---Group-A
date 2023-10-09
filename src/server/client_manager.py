"""Module for managing a connection from a client"""
# Idea and outline: Miguel Valadas
# Message Protocol: Miguel Valadas
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023

import json
import os
import uuid
from datetime import datetime

from src.util.branston import Branston
from src.util.crypt import Crypt
from src.util.enums import ServerDestination, Source, SecurityLevel, Format


class ClientManager:
    """ClientManager Class handles connection from Client"""
    ENCODING_FORMAT = 'utf-8'
    # Using big-endian, i.e., the most significant byte is at the beginning of the array (like a regular book).
    # It is important to use big-endian because Branston Protocol expects data in a certain order
    BYTE_ORDER = 'big'

    def __init__(self, sock, destination, output_directory):
        self.pickling_format = None
        self.socket = sock
        # Settings from Server Wizard
        self.data_destination = destination
        self.output_directory = output_directory
        # Data settings
        self.data_source = None
        self.security_level = None
        # Data Processors
        self.crypt = Crypt.new_keys()
        self.pickler = Branston()
        self.message = None
        self.received_data = None
        self.decrypted_data = None
        self.processed_data = None
        self.has_acknowledged_client = False

    def run(self):
        """Control procedure handling receipt of data from client"""
        while True:
            try:
                # Get the length of the upcoming message
                length_data = self.socket.recv(4)
                if not length_data:  # If length_data is empty, the client has disconnected.
                    print(f"[{datetime.now()}] - Client has disconnected.")
                    break

                # Convert the received message length to an int, using big-endian for the byte order
                message_length = int.from_bytes(length_data, self.BYTE_ORDER)
                self.message = self.socket.recv(message_length)

                if not self.message:
                    print(f"[{datetime.now()}] - Client has disconnected.")
                    break

                self.parse_message()

            except Exception as e:
                print(f"[{datetime.now()}] - Error occurred: {e}")
                break

    def parse_message(self):
        """What shall I do with this communication?"""
        if len(self.message) == 3:  # Check if it's an init message
            self.apply_client_settings()
            self.__acknowledge_client()
            return

        if self.message.endswith(b"END"):
            self.message = self.message[:-3]

        if self.pickling_format != Format.BINARY.value and self.security_level != SecurityLevel.Encrypted.value:
            try:
                decoded_message = self.message.decode(self.ENCODING_FORMAT)
                self.received_data = decoded_message
            except UnicodeDecodeError:
                print("Error: Unable to decode the message.")
                return
        else:
            self.received_data = self.message
        try:
            self.decrypt_data()
            self.process_by_source()
            self.output()
        except Exception as e:
            print(f"Error: {e}")

    def apply_client_settings(self):
        self.pickling_format = int.from_bytes(self.message[:1], self.BYTE_ORDER)
        if self.pickling_format != 0:
            self.pickler.set_pickling_format(self.pickling_format)
        self.data_source = int.from_bytes(self.message[1:2], self.BYTE_ORDER)
        self.security_level = int.from_bytes(self.message[2:3], self.BYTE_ORDER)

    def __acknowledge_client(self):
        if self.security_level == SecurityLevel.Encrypted.value:
            pub_key_data = {
                'modulus': self.crypt.get_public_key().n,
                'exponent': self.crypt.get_public_key().e
            }
            message = f"ACK{json.dumps(pub_key_data)}END"
        else:
            message = "ACKNULLEND"

        message_bytes = message.encode(self.ENCODING_FORMAT)
        length = len(message_bytes)

        self.socket.send(length.to_bytes(4, self.BYTE_ORDER) + message_bytes)
        self.has_acknowledged_client = True

    def _await_payload(self):
        length_data = self.socket.recv(4)
        message_length = int.from_bytes(length_data, self.BYTE_ORDER)
        self.message = self.socket.recv(message_length)

        if self.pickling_format != Format.BINARY.value or not self.has_acknowledged_client:
            self.message = self.message.decode(self.ENCODING_FORMAT)
        self.parse_message()

    def decrypt_data(self):
        """Decrypts the received data if required"""
        if self.security_level == SecurityLevel.Encrypted.value and self.data_source == Source.TextFile.value:
            self.decrypted_data = self.crypt.decrypt(self.received_data)
        else:
            self.decrypted_data = self.received_data

    def process_by_source(self):
        """Calls appropriate processing"""
        if self.data_source == Source.TextFile.value:
            self.process_textfile()
        elif self.data_source == Source.Dictionary.value:
            self.process_dictionary()

    def process_textfile(self):
        """Runs processes required for textfiles"""
        if self.decrypt_data is not None:
            self.processed_data = self.decrypted_data
        else:
            self.processed_data = self.received_data

    def process_dictionary(self):
        """Runs processes required for Dictionaries"""
        # Unpickle the dictionary
        self.processed_data = self.pickler.unpickle(self.received_data)

    def output(self):
        """Outputs the data to console or textfile as per server setting"""
        if self.data_destination == ServerDestination.Print:
            print(f"[{datetime.now()}] - {self.processed_data}")
        if self.data_destination == ServerDestination.File:
            self.output_to_textfile()
        self.has_acknowledged_client = False

    @staticmethod
    def get_new_filepath(output_directory):
        """Returns a new unique filename and path"""
        my_uuid = uuid.uuid4().hex
        file_name = f'{my_uuid}.txt'
        file_path = os.path.join(output_directory, file_name)
        return file_path

    def output_to_textfile(self):
        """Writes a textfile with the unpickled data"""
        file_path = self.get_new_filepath(self.output_directory)
        with open(file_path, "w") as outfile:
            outfile.write(f"[{datetime.now()}] - {self.processed_data}")
