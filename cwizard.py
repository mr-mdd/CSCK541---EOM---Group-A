"""Module to help the user build a dictionary and choose options"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 29/09/2023
from enums import *
import os


class ClientWizard:
    """Class to gather user options"""

    def __init__(self):
        self.source = None
        self.format = None
        self.dictionary = dict()
        self.filepath = None
        self.security = None

    # Question 1
    def choose_source(self):
        """Asks the user for the data source"""
        print("\nDo you want to send a dictionary or a textfile?")
        response = input("d/t: ")
        match response:
            case "d":
                print("You selected dictionary")
                self.source = Source.Dictionary
            case "t":
                print("You selected textfile")
                self.source = Source.TextFile
            case _:
                print("Invalid source")
                self.choose_source()

    def choose_format(self):
        """Asks the user for the pickling format"""
        print("\nChoose a pickling format: Binary, JSON, or XML")
        response = input("b/j/x: ")
        match response:
            case "b":
                print("You selected binary")
                self.format = Format.BINARY
            case "j":
                print("You selected json")
                self.format = Format.JSON
            case "x":
                print("You selected XML")
                self.format = Format.XML
            case _:
                print("Invalid pickling format")
                self.choose_format()

    def choose_textfile(self):
        """Asks the user to select the filepath to the textfile"""
        print("\nPlease input the filepath to the textfile")
        response = input("filepath: ")
        if os.path.exists(response):
            self.filepath = response
        else:
            print("Invalid filepath")
            self.choose_textfile()

    def choose_security(self):
        """Asks the user to select the security option"""
        print("\nDo you want to encrypt the file?")
        response = input("y/n: ")
        match response:
            case "y":
                print("You chose to encrypt the file")
                self.security = SecurityLevel.Encrypted
            case "n":
                print("You chose not to encrypt the file")
                self.security = SecurityLevel.UnEncrypted
            case _:
                print("Invalid security level")
                self.choose_security()

    def build_dictionary(self):
        """Builds a dictionary item by item"""
        print("\nNow we will build the dictionary")
        item = 1
        flag = True
        while flag:
            key = input(f"\nItem {item} key: ")
            value = input(f"Item {item} value: ")
            self.dictionary.update({key: value})
            response = input("type 'x' if that was your last item: ")
            if response == "x":
                flag = False
            else:
                item += 1

    def ask_all(self):
        """Runs the Wizard"""
        print("\n*** Welcome to the client Wizard ***")
        self.choose_source()
        # Dictionary
        if self.source == Source.Dictionary:
            self.choose_format()
            self.build_dictionary()
        # Textfile
        else:
            self.choose_textfile()
            self.choose_security()

    def display(self):
        """Displays a summary of the User Inputs"""
        print("\nUser Input Summary:\n")

        if self.source is not None:
            print("Source:", self.source.name)

        if self.format is None:
            print("Format:")
        else:
            print("Format:", self.format.name)
            print("Dictionary:", self.dictionary)

        if self.filepath is not None:
            print("Filepath:", self.filepath)
            print("Security:", self.security.name)
        else:
            print("Filepath:")
            print("Security:")
