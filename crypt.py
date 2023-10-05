"""Module handling Encryption and Decryption"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 30/09/2023
# Reference: https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
# Reference: https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-implement-multiple-constructors
# Reference: https://pythonw3schools.com/data-hiding-in-python/

import rsa


class Crypt:
    """Class for asymmetrical encryption"""

    @classmethod
    def new_keys(cls):
        """Returns the class initialised with new Public and Private Keys for decryption"""
        return cls(None)

    @classmethod
    def with_key(cls, public_key):
        """Returns the class initialised with a Public Key for encryption only"""
        return cls(public_key)

    def __init__(self, public_key):
        if public_key is None:
            # Generates new public and private keys
            self._public_key, self.__private_key = rsa.newkeys(512)
        else:
            # Applies a given public key
            self._public_key = public_key
            self.__private_key = None

    def get_public_key(self):
        """Attribute Getter for Public Key"""
        return self._public_key

    def encrypt(self, data):
        """Returns encrypted data"""
        return rsa.encrypt(data.encode(), self._public_key)

    def decrypt(self, data):
        """Returns decrypted data"""
        if self.__private_key is None:
            raise Exception("Functionality requires Private Key")
        else:
            return rsa.decrypt(data, self.__private_key).decode()
