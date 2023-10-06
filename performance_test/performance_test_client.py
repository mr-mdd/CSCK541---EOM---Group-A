from src.util.branston import Branston
import socket
from src.client.client import Client
from src.util.enums import SecurityLevel, Source
from src.util.crypt import Crypt
from src.client.client_wizard import ClientWizard

import timeit



# Performance test to verify the application on the time taken on various tasks.

# Test 1: Performace test on serializing the provided dictionary data based on the specified format-JSON

test_serializing= timeit.Timer(
    lambda: _choose_format()).repeat(number=10000)
print("The time taken for serializing is", test_serializing)

# Test 2: Performace test on encrypting the provided file content 

test_encrypting= timeit.Timer(
    lambda: _choose_security()).repeat(number=10000)
print("The time taken for encrypting the provided file content is", test_encrypting)

# Test 3: Performace test on reading the content of a file specified by the file path

test_reading= timeit.Timer(
    lambda: _choose_textfile()).repeat(number=10000)
print("The time taken for reading the content of a file specified by the file path is", test_reading)

# Test 4: Performace test on establishing a connection with the server

test_server_connection= timeit.Timer(
    lambda: connect()).repeat(number=10000)
print("The time taken for establishing a connection with the server is", test_server_connection)
