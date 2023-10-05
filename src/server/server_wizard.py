"""Module to help the user initialise the server"""
import os
import socket
import server

# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
from src.util.enums import ServerClients, ServerDestination


class ServerSettings:
    """Struct which will be used to pass instantiation values the Server"""
    client_source = None
    port_number = None
    data_destination = None
    output_dir = None


class ServerWizard:
    """Class to initialise the server"""

    def __init__(self):
        self._server_settings = ServerSettings()

    def get_server_settings(self):
        """Attribute getter for the server settings object"""
        return self._server_settings

    def _choose_clients(self):
        """Ask the user whether to accept clients from other computers"""
        print("\Please configure the Branston Server for clients on a single PC or multiple PCs")
        response = input("s/m: ")
        # Input Validation
        if response not in "sm":
            "Invalid client source"
            self._choose_clients()
        elif response == "s":
            self._server_settings.client_source = ServerClients.SinglePC
        else:
            self._server_settings.client_source = ServerClients.MultiPC

    def _choose_port(self):
        """Asks the user to input the port number"""
        print("\nPlease choose the Server Port")
        response = input("Number (1 - 65535): ")
        # Input Validation - must be a number and must be between 1023 and 65535
        # 1 to 1023 are reserved ports
        if response.isnumeric and int(response) in range(1024, 65535):
            self._server_settings.port_number = int(response)
        else:
            print("Invalid Port Number")
            self._choose_port()

        # Second-Stage Validation - Check if port is in use
        if not self._check_port(self._server_settings.port_number):
            print(f"Port {self._server_settings.port_number} is unavailable")
            self._choose_port()

    # Reference: https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python
    @staticmethod
    def _check_port(port_number):
        """Checks to see if a port number is available"""

        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            test_socket.bind(("127.0.0.1", port_number))
            retval = True
        except socket.error:
            retval = False
        finally:
            test_socket.close()
        return retval

    def _choose_output(self):
        """Asks the user to select the output option"""
        print("\nPlease choose to output received data to console or textfile")
        response = input("c/t: ")
        match response:
            case "c":
                self._server_settings.data_destination = ServerDestination.Print
            case "t":
                self._server_settings.data_destination = ServerDestination.File
            case _:
                print("Invalid data destination")
                self._choose_output()

    def _choose_output_directory(self):
        """Asks the user to select the output directory"""
        print("\nPlease choose where to save textfiles")
        response = input("directory: ")
        if os.path.exists(response):
            self._server_settings.filepath = response
        else:
            print("Invalid filepath")
            self._choose_output_directory()

    def ask_all(self):
        """Runs the Wizard"""
        print("\n*** Welcome to the server Wizard ***")
        self._choose_clients()
        self._choose_port()
        self._choose_output()
        self._choose_output_directory()

    def display(self):
        """Displays a summary of the User Inputs"""
        print("\nUser Input Summary:\n")

        if self._server_settings.port_number is not None:
            print(f"Port Number: {self._server_settings.port_number}")

        if self._server_settings.data_destination is not None:
            print(f"Output Destination: {self._server_settings.data_destination}")

        if self._server_settings.output_dir is not None:
            print(f"Textfile Directory: {self._server_settings.output_dir}")


if __name__ == "__main__":
    my_server_wizard = ServerWizard()
    my_server_wizard.ask_all()
    my_server = server.Server(my_server_wizard.get_server_settings())
    my_server.listen()
