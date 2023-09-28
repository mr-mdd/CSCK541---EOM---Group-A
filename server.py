"""Module for receiving data from client"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 28/09/2023
# Reference: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
# Reference: https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python
# TODO: Add multi-threading

from branston import Branston
import socket
from enums import *
from crypt import Crypt
import os
import uuid


class Server:
    PORT_NUMBER = 30687  # Port Number (# days of Saturn's Orbit, in case you were wondering)
    BACKLOG = 5  # Required for Listen
    BUFFER_SIZE = 1024

    def __init__(self):
        self._received_data = ""
        self._processed_data = None
        self.pickler = Branston()

        # Default to Printing
        self._destination = ServerDestination.Print

        # Set Default Output Directory
        self._output_directory = os.path.dirname(os.path.realpath(__file__))
        default_dir = self.get_default_dir()
        self.set_output_directory(default_dir)

        # Default to Dictionary
        self._data_source = Source.Dictionary

        # Default to not encrypted
        self._crypt = Crypt.server()
        self._security = SecurityLevel.UnEncrypted

    def get_security(self):
        """Attribute Getter for whether data is encrypted"""
        return self._security

    def set_security(self, security):
        """Attribute Setter for whether data is encrypted"""
        if security in SecurityLevel:
            self._security = security
        else:
            raise Exception("Invalid security level")

    @staticmethod
    def get_default_dir():
        """Returns default directory for saving textfiles"""
        current = os.path.dirname(os.path.realpath(__file__))
        output = os.path.join(current, "Output")
        return output

    def get_output_directory(self):
        """Attribute Getter for Output Directory"""
        return self._output_directory

    def set_output_directory(self, directory):
        """Attribute Setter for the directory where textfiles will be written"""
        # Ensure Directory exists
        if not os.path.isdir(directory):
            os.mkdir(directory)
        # Set Attribute
        self._output_directory = directory

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

            # Filter data for message or content
            data = self.filter_data(data, conn)

            if data is not None:
                print("Server received", repr(data))
                self._received_data = data
                self.decision_tree()
                conn.send(Conversation.DataReceived)

            conn.close()

    def filter_data(self, message, connection):
        """Is the incoming data a message or data?"""

        # Is this a message? If so perform action
        if message in Conversation:
            match message:
                case Conversation.CanISendData:
                    connection.send(Conversation.SendDataFormat)
                case Conversation.SendDataFormat:
                    pass  # Client Side Only
                case Conversation.PublicKeyReceived:
                    connection.send(Conversation.SendData)
                case Conversation.SendData:
                    pass  # Client Side Only
                case Conversation.DataReceived:
                    pass  # Client Side Only

            return None

        # Are these settings?
        elif 16 <= int(message) < 128:
            self.parse_settings(message)
            if self._security == SecurityLevel.UnEncrypted:
                connection.send(Conversation.SendData)
            return None

        # If not a message then this is data
        else:
            return message

    def parse_settings(self, total):
        """Parses settings from client for Security Level, Data Source, and Data Format"""
        # I'm pretty sure there is a better bitwise method of doing this,
        # but it works
        # Edit: I tried the bitwise version and I don't think it is superior
        # It is also less readable than this version.

        # Security
        if total >= SecurityLevel.Encrypted:
            self.set_security(SecurityLevel.Encrypted)
        elif total >= SecurityLevel.UnEncrypted:
            self.set_security(SecurityLevel.UnEncrypted)

        # Remove either Security Value
        total = total % SecurityLevel.UnEncrypted

        # Source Type
        if total >= Source.TextFile:
            self.set_source(Source.TextFile)
        elif total >= Source.Dictionary:
            self.set_source(Source.Dictionary)

        # Remove either Source Type
        total = total % Source.Dictionary

        # Format
        if total > 0:
            self.set_pickling_format(Format(total))

    def decision_tree(self):
        # What kind of data is it?
        if self._data_source == Source.TextFile:
            # Handle Textfiles
            if self._security == SecurityLevel.Encrypted:
                # Handle Encrypted File
                self._processed_data = self._crypt.decrypt(self._received_data)
            else:
                # Handle Unencrypted File
                self._processed_data = self._received_data
        else:
            # Handle Dictionaries
            self._processed_data = self.pickler.unpickle(self._received_data)

        # Where should the data be sent to?
        if self._destination == ServerDestination.Print:
            # Handle Print
            self.output_to_console()
        else:
            # Handle Saving to Textfile
            self.output_to_textfile()

    def get_new_filepath(self):
        my_uuid = uuid.uuid4().hex
        file_name = f'{my_uuid}.txt'
        file_path = os.path.join(self._output_directory, file_name)
        return file_path

    def output_to_console(self):
        print(self._processed_data)

    def output_to_textfile(self):
        """Writes a textfile with the unpickled data"""
        file_path = self.get_new_filepath()
        with open(file_path, "w") as outfile:
            outfile.write(self._processed_data)
