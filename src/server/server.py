"""Module for a multi-threaded Server"""
# Author: Miguel Valadas
# Edited to conform to project style: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
import socket
import threading
from datetime import datetime

from src.server.client_manager import ClientManager
from src.util.enums import ServerClients


class Server:
    """Class definition for multi-threaded server"""
    BACKLOG = 5  # Required for Listen

    def __init__(self, settings):
        # Apply Settings from Wizard
        self.port_number = settings.port_number
        self.data_destination = settings.data_destination
        self.output_directory = settings.output_dir

        self.socket = socket.socket()
        if settings.client_source == ServerClients.SinglePC:
            # Accept only clients on localhost
            self.socket.bind(("127.0.0.1", self.port_number))
        else:
            # Accept clients from any PC
            self.socket.bind(self.port_number)

    def listen(self):
        """Accepts new clients and starts new thread for each"""
        self.socket.listen(self.BACKLOG)
        print(f"[{datetime.now()}] - Branston Server is listening on Port: {self.port_number}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"[{datetime.now()}] - Connection Accepted from {client_address}")
            new_connection = ClientManager(client_socket, self.data_destination, self.output_directory)
            threading.Thread(target=new_connection.run).start()
