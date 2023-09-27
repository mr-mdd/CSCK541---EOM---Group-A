"""Module handling Encryption and Decryption"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 27/09/2023
# Reference: https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
# Reference: https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-implement-multiple-constructors

import rsa


class Crypt:
    """Class for asymmetrical encryption"""

    @classmethod
    def server(cls):
        return cls(None)

    @classmethod
    def client(cls, public_key):
        return cls(public_key)

    def __init__(self, public_key):
        if public_key is None:
            # Generates new public and private keys for Server
            self._public_key, self._private_key = rsa.newkeys(512)
            self._server = True
        else:
            # Applies a given public key for Client
            self._public_key = public_key
            self._private_key = None
            self._server = False

    def get_public_key(self):
        """Attribute Getter for Public Key"""
        return self._public_key

    def encrypt(self, data):
        """Returns encrypted data"""
        return rsa.encrypt(data.encode(), self._public_key)

    def decrypt(self, data):
        """Returns decrypted data"""
        if self._server:
            return rsa.decrypt(data, self._private_key).decode()
        else:
            raise Exception("Functionality not available Client Side")
