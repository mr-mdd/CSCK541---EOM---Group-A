"""Module for multi-format Serialization"""
from enum import Enum
import pickle
import json
import dict2xml
from dicttoxml import dicttoxml
import xmltodict
from crypt import Crypt

# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 27/09/2023
# Reference: https://docs.python.org/3/library/pickle.html
# Reference: https://www.digitalocean.com/community/tutorials/python-pickle-example

"""
Requirements - from Task - awaiting official requirements document
    
    Source
    - Dictionary
    - Text File
    
    - Serialise and send to Server

    Serialisation and deserialisation options for Dictionary
    - Binary: Pickle
    - JSON
    - XML
    
    Encryption option for text file
    
    Option for Server to print received items to screen or file

"""


class Format(Enum):
    BINARY = 1
    JSON = 2
    XML = 3


class Source(Enum):
    Dictionary = 4
    TextFile = 8


class Branston:
    """Class definition for multi-format serialisation"""

    # Non-UK folks... Branston is a UK-brand of sweet pickle - like chutney

    def __init__(self):
        # Default to Dictionary
        self._source_type = Source.Dictionary
        # Default to Binary Format
        self._pickling_format = Format.BINARY
        self._write_format = "wb"
        self._read_format = "rb"
        self._serialisation_function = pickle.dumps
        self._deserialisation_function = pickle.loads
        self._filepath = "test.pck"
        # Default to Not Encrypted
        self._encrypted = False
        # Default to Print

    def get_source_type(self):
        """Attribute Getter for whether source is Dictionary or Text File"""
        return self._source_type

    def set_source_type(self, source_type):
        """Attribute Setter for source type"""
        if source_type in Source:
            self._source_type = source_type
        else:
            raise Exception("Invalid Source Type")

    def get_encrypted_flag(self):
        """Attribute Getter for whether data is encrypted"""
        return self._encrypted

    def set_encrypted_flag(self, encrypt):
        """Attribute Setter for whether data is encrypted"""
        if encrypt in (True, False):
            self._encrypted = encrypt
        else:
            raise Exception("Invalid encrypted flag")

    def get_pickling_format(self):
        """Attribute Getter for the Pickling Format"""
        return self._pickling_format

    def set_pickling_format(self, pickling_format):
        """Attribute Setter for the Pickling Format"""
        self._pickling_format = pickling_format

        match pickling_format:
            case Format.BINARY:
                self._write_format = "wb"
                self._read_format = "rb"
                self._serialisation_function = pickle.dumps
                self._deserialisation_function = pickle.loads

            case Format.JSON:
                self._write_format = "w"
                self._read_format = "r"
                self._serialisation_function = json.dumps
                self._deserialisation_function = json.loads

            case Format.XML:
                self._write_format = "w"
                self._read_format = "r"
                self._serialisation_function = dicttoxml
                # self._serialisation_function = dict2xml.dict2xml
                self._deserialisation_function = xmltodict.unparse

            case _:
                raise Exception("Invalid Pickling Format")

    def pickle(self, data):
        pass

    def unpickle(self, data):
        pass

    def encrypt(self, data):
        return Crypt.encrypt(data)

    def decrypt(self, data):
        return Crypt.decrypt(data)

    def write_to_file(self, data):
        with open(self._filepath, self._write_format) as outfile:
            outfile.write(data)
