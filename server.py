"""Module for a multi-threaded Server"""
# Author: Miguel Valadas
# Edited to conform to project style: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
import socket
import threading
from client_manager import ClientManager
from enums import ServerClients


"""
Comment:
I think MV put in the self.connections list as a stub for
future monitoring functionality.
It does not do anything currently, but I'm leaving it as a stub for now.
MV to confirm.
DD
"""


class Server:
    """Class definition for multi-threaded server"""
    BACKLOG = 5  # Required for Listen

    def __init__(self, settings):
        # Apply Settings from Wizard
        self.port_number = settings.port_number
        self.data_destination = settings.data_destination
        self.output_directory = settings.output_dir

        # Create the Socket
        """
        Comment:
        This line broke the code, but it works without the arguments.
        DD
        """
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = socket.socket()
        if settings.client_source == ServerClients.SinglePC:
            # Accept only clients on localhost
            self.socket.bind(("127.0.0.1", self.port_number))
        else:
            # Accept clients from any PC
            self.socket.bind(self.port_number)

        # Client Connections
        self.connections = []  # Not currently in use

    def listen(self):
        """Accepts new clients and starts new thread for each"""
        self.socket.listen(self.BACKLOG)
        print(f"Branston Server is listening on Port: {self.port_number}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection Accepted from {client_address}")
            new_connection = ClientManager(client_socket, self.data_destination, self.output_directory)
            # Add the new connection to the collection - not currently used for anything
            self.connections.append(new_connection)
            threading.Thread(target=new_connection.run).start()
