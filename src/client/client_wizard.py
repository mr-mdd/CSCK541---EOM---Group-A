"""Module to help the user build a dictionary and choose options"""
import uuid

from src.client import client
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023
# Reference: https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
# Reference: https://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
from src.util.enums import Source, Format, SecurityLevel
import os
import ipaddress


# import tempfile  # required for alternative method


class ClientSettings:
    """Struct which will be used to pass instantiation values the Client"""
    hostname = None
    port_number = None
    source = None
    data_format = None
    dictionary = dict()
    filepath = None
    security_level = None


class ClientWizard:
    """Class to gather user options"""

    def __init__(self):
        self._settings = ClientSettings()
        self._textfile_dir = None

    def get_client_settings(self):
        """Attribute getter for the client settings object"""
        return self._settings

    def _choose_host(self):
        """Asks the user to input the Server"""
        print("\nPlease type the hostname of the Server")
        response = input("Server: ")
        # Input Validation - must not be blank
        if self.is_valid_ipaddress(response):
            self._settings.hostname = response
        else:
            print("Invalid Host")
            self._choose_host()

    @staticmethod
    def is_valid_ipaddress(address):
        """Validates given IP Address"""
        try:
            ip = ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    def _choose_port(self):
        """Asks the user to input the port number"""
        print("\nPlease choose the Server Port")
        response = input("Number (1 - 65535): ")
        # Input Validation - must be a number and must be between 1 and 65535
        # 1 to 1023 are reserved ports
        if response.isnumeric and int(response) in range(1024, 65535):
            self._settings.port_number = int(response)
        else:
            print("Invalid Port Number")
            self._choose_port()

    def _choose_source(self):
        """Asks the user for the data source"""
        print("\nDo you want to send a dictionary or a textfile?")
        response = input("d/t: ")
        match response:
            case "d":
                print("You selected dictionary")
                self._settings.source = Source.Dictionary
            case "t":
                print("You selected textfile")
                self._settings.source = Source.TextFile
            case _:
                print("Invalid source")
                self._choose_source()

    def _choose_format(self):
        """Asks the user for the pickling format"""
        print("\nChoose a pickling format: Binary, JSON, or XML")
        response = input("b/j/x: ")
        match response:
            case "b":
                print("You selected binary")
                self._settings.data_format = Format.BINARY
            case "j":
                print("You selected json")
                self._settings.data_format = Format.JSON
            case "x":
                print("You selected XML")
                self._settings.data_format = Format.XML
            case _:
                print("Invalid pickling format")
                self._choose_format()

    def _choose_textfile(self):
        """Asks the user to select the filepath to the textfile"""
        print("\nPlease input the filepath to the textfile")
        response = input("filepath: ")
        if os.path.exists(response):
            self._settings.filepath = response
        else:
            print("Invalid filepath")
            self._choose_textfile()

    def _choose_security(self):
        """Asks the user to select the security option"""
        print("\nDo you want to encrypt the file?")
        response = input("y/n: ")
        match response:
            case "y":
                print("You chose to encrypt the file")
                self._settings.security_level = SecurityLevel.Encrypted
            case "n":
                print("You chose not to encrypt the file")
                self._settings.security_level = SecurityLevel.Plain
            case _:
                print("Invalid security level")
                self._choose_security()

    def _build_dictionary(self):
        """Builds a dictionary item by item"""
        print("\nNow we will build the dictionary")
        item = 1
        flag = True
        while flag:
            key = input(f"\nItem {item} key: ")
            value = input(f"Item {item} value: ")
            self._settings.dictionary.update({key: value})
            response = input("type 'x' if that was your last item: ")
            if response == "x":
                flag = False
            else:
                item += 1

    def ask_all(self):
        """Runs the Wizard"""
        print("\n*** Welcome to the client Wizard ***")

        # Settings for Connection to Server
        self._choose_host()
        self._choose_port()

        self._choose_source()
        # Dictionary
        if self._settings.source == Source.Dictionary:
            self._choose_format()
            self._build_dictionary()
        # Textfile
        else:
            # self._choose_textfile()
            self._ask_textfile_questions()
            # moved below so that either Source may be encrypted
            # self._choose_security()

        self._choose_security()

    def _ask_textfile_questions(self):
        print("\nDo you want to upload an existing textfile?")
        response = input("y/n: ")
        # Validate input
        if response not in "yn":
            print("Invalid option entered")
            self._ask_textfile_questions()

        if response == "y":
            # Choose existing textfile
            self._choose_textfile()
        else:
            # build a new textfile
            self._choose_textfile_directory()
            self._build_textfile()

    def _choose_textfile_directory(self):
        """Asks the user to select the output directory for created textfiles"""
        # Leaving this here for alternative approach of saving file to temp directory
        # temp_dir = tempfile.gettempdir()

        print("\nPlease choose where to save textfiles")
        response = input("directory: ")
        if os.path.exists(response):
            self._textfile_dir = response
        else:
            print("Invalid filepath")
            self._choose_textfile_directory()

    def get_new_filepath(self):
        """Returns a new unique filename and path"""
        my_uuid = uuid.uuid4().hex
        file_name = f'{my_uuid}.txt'
        file_path = os.path.join(self._textfile_dir, file_name)
        return file_path

    def _build_textfile(self):
        # create a new textfile
        self._settings.filepath = self.get_new_filepath()
        with open(self._settings.filepath, "w") as outfile:

            """Builds a textfile line by line"""
            print("\nNow we will build the textfile")
            item = 1
            flag = True
            while flag:
                # Line input by user
                line_text = input(f"\nLine {item} text: ")
                # Add line to textfile
                outfile.write(line_text)
                outfile.write("\n")

                response = input("type 'x' if that was your last line: ")
                if response == "x":
                    flag = False
                else:
                    item += 1

    def display(self):
        """Displays a summary of the User Inputs"""
        print("\nUser Input Summary:\n")

        print(f"Hostname: {self._settings.hostname}")
        print(f"Port: {self._settings.port_number}")

        if self._settings.source is not None:
            print(f"Source: {self._settings.source.name}")

        if self._settings.data_format is None:
            print("Format:")
        else:
            print(f"Format: {self._settings.data_format.name}")
            print(f"Dictionary: {self._settings.dictionary}")

        print(f"Filepath: {self._settings.filepath}")
        print(f"Security: {self._settings.security_level.name}")


if __name__ == "__main__":
    my_client_wizard = ClientWizard()
    my_client_wizard.ask_all()
    my_client_wizard.display()
    my_client = client.Client(my_client_wizard.get_client_settings())
    my_client.connect()
