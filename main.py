"""Module for running the Branston Classes"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 29/09/2023

import branston
import client
from crypt import Crypt
import server
from enums import *
from cwizard import ClientWizard


# Pickle Unit Tests ********************************************************
# my_pickler = branston.Branston()
# my_pickler.set_pickling_format(Format.XML)
# my_pickler.set_source_type(Source.Dictionary)

# my_client = client.Client()
# my_server = server.Server()


# Crypt Unit Tests *********************************************************
# my_crypt_server = Crypt.server()
# public_key = my_crypt_server.get_public_key()
# my_crypt_client = Crypt.client(public_key)
# text = "'Ello, I wish to register a complaint"
# print(text)
# encrypted = my_crypt_client.encrypt(text)
# print(encrypted)
# decrypted = my_crypt_server.decrypt(encrypted)
# print(decrypted)


# Server Dynamic Filepath Tests *******************************************
# my_server = server.Server()
# print(my_server.get_output_directory())
# print(my_server.get_new_filepath())

# Bitwise identification of settings
# settings = Format.BINARY.value + Source.Dictionary.value + SecurityLevel.Encrypted.value
# print(settings)
# bsettings = bin(settings)
# print(bsettings)
# print('dictionary: ', bsettings[-3])    # 4
# print('textfile: ', bsettings[-4])      # 8
# print('Unencrypted: ', bsettings[-5])   # 16
# print('Encrypted: ', bsettings[-6])     # 32
# Is this really an improvement?

# User Wizard Test
my_wizard = ClientWizard()
my_wizard.ask_all()
my_wizard.display()
