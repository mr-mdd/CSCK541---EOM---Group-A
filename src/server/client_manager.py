"""Module for managing a connection from a client"""
# Idea and outline: Miguel Valadas
# Message Protocol: Miguel Valadas
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
import os
import uuid
from src.util.enums import ServerDestination, Source, SecurityLevel
from src.util.crypt import Crypt
from src.util.branston import Branston


class ClientManager:
    """ClientManager Class handles connection from Client"""
    BUFFER = 1024  # does anyone know why this value? or should it be changed?

    def __init__(self, sock, destination, output_directory):
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
        # Instance Variables
        self.message = None
        self.parts = None
        self.received_data = None
        self.decrypted_data = None
        self.processed_data = None

    def run(self):
        """Control procedure handling receipt of data from client"""
        self.message = self.socket.recv(self.BUFFER).decode('utf-8')
        self.parse_message()

    def parse_message(self):
        """What shall I do with this communication?"""

        self.parts = self.message.split('\0')

        # Message Protocol 1: Client - Initialization Message
        # Initial request has 3 elements
        if len(self.parts) == 3:
            # This is an initial request
            self.apply_client_settings()
            self.acknowledge_client()

        # Message Protocol 3: Payload Message (post-ACK)
        # Payload has last element of END
        elif self.parts[-1] == "END":
            # This is the payload
            self.received_data = self.parts[-2]
            self.decrypt_data()
            self.process_by_source()
            self.output()

        # This is a spurious message - do not process
        else:
            print("Message does not conform to Branston protocol")

    def apply_client_settings(self):
        if self.parts[0] is not None:
            self.pickler.set_pickling_format(self.parts[0])
        self.data_source = self.parts[1]
        self.security_level = self.parts[2]

    def acknowledge_client(self):
        if self.security_level == SecurityLevel.Encrypted:
            # Message Protocol 2.1: Acknowledge message with Public Key
            message = f"\0ACK\0[{self.crypt.get_public_key()}]\0"
        else:
            # Message Protocol 2.2: Acknowledge message without Public Key
            message = "\0ACK%NULL\0"
        self.socket.send(message)

    def decrypt_data(self):
        """Decrypts the received data if required"""
        if self.security_level == SecurityLevel.Encrypted:
            self.decrypted_data = self.crypt.decrypt(self.received_data)
        else:
            self.decrypted_data = self.received_data

    def process_by_source(self):
        """Calls appropriate processing"""
        if self.data_source == Source.TextFile:
            self.process_textfile()
        if self.data_source == Source.Dictionary:
            self.process_dictionary()

    def process_textfile(self):
        """Runs processes required for textfiles"""
        # Removed decryption from here
        # Left as stub if functionality added
        pass

    def process_dictionary(self):
        """Runs processes required for Dictionaries"""
        # Unpickle the dictionary
        self.processed_data = self.pickler.unpickle(self.received_data)

    def output(self):
        """Outputs the data to console or textfile as per server setting"""
        if self.data_destination == ServerDestination.Print:
            print(self.processed_data)
        if self.data_destination == ServerDestination.File:
            self.output_to_textfile()

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
            outfile.write(self.processed_data)
