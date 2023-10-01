"""Module for running the Branston Classes"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 29/09/2023

from crypt import Crypt


# Crypt Driver Code *********************************************************
my_crypt_server = Crypt.server()
public_key = my_crypt_server.get_public_key()
my_crypt_client = Crypt.client(public_key)
text = "'Ello, I wish to register a complaint"
print(text)
encrypted = my_crypt_client.encrypt(text)
print(encrypted)
decrypted = my_crypt_server.decrypt(encrypted)
print(decrypted)
