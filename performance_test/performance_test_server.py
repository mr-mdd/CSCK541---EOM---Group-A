import socket
import threading
from src.server.client_manager import ClientManager
from src.util.enums import ServerClients
from src.server.server_wizard import ServerWizard

import timeit



# Performance test to verify the application on the time taken on various tasks.

# Test 1: Performace test on deserializing the received data based on the specified format

test_output= timeit.Timer(
    lambda: _choose_output()).repeat(number=10000)
print("The time taken for outputing received data to console is", test_output)

# Test 2: Performace test on decrypting the provided encrypted content 

test_decrypting= timeit.Timer(
    lambda: _choose_clients()).repeat(number=10000)
print("The time taken for populating dictionary is", test_decrypting)

# Test 3: Performace test on listening for incoming connections from client

test_listening= timeit.Timer(
    lambda: listen
print("The time taken for listening for incoming connections from client is", test_listening)
