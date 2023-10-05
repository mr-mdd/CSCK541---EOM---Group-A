"""Module for multi-format Serialization"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 29/09/2023
# Reference: https://docs.python.org/3/library/pickle.html
# Reference: https://www.digitalocean.com/community/tutorials/python-pickle-example

import pickle
import json
# import dict2xml
from dicttoxml import dicttoxml
import xmltodict

from src.util.enums import Format


class Branston:
    """Class definition for multi-format serialisation of dictionary"""

    # Non-UK folks... Branston is a UK-brand of sweet pickle - like chutney

    def __init__(self):
        # Default to Binary Format
        self._pickling_format = Format.BINARY
        self._write_format = "wb"
        self._read_format = "rb"
        self._serialisation_function = pickle.dumps
        self._deserialisation_function = pickle.loads

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
                # TODO: xmltodict does not work with xml documents created by either of the above
                # known error: Must have exactly one root
                self._deserialisation_function = xmltodict.unparse

            case _:
                raise Exception("Invalid Pickling Format")

    def pickle(self, data):
        """Returns a pickled bytes object"""
        return self._serialisation_function(data)

    def unpickle(self, data):
        """Returns an unpickled string of the data"""
        return self._deserialisation_function(data)
