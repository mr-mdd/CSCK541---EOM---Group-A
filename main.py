"""Module for running the Branston Classes"""
import branston
import client
from crypt import Crypt
import server
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 27/09/2023

from branston import Format, Source


# Unit Tests
# my_pickler = branston.Branston()
# my_pickler.set_pickling_format(Format.XML)
# my_pickler.set_source_type(Source.Dictionary)

# my_client = client.Client()
# my_server = server.Server()

my_crypt_server = Crypt.server()
public_key = my_crypt_server.get_public_key()

my_crypt_client = Crypt.client(public_key)

text = "'Ello, I wish to register a complaint"
print(text)
encrypted = my_crypt_client.encrypt(text)
print(encrypted)
decrypted = my_crypt_server.decrypt(encrypted)
print(decrypted)
