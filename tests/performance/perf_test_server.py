import timeit
from unittest.mock import Mock
from src.server.client_manager import ClientManager
from src.server.server_wizard import ServerWizard
from src.server.server import Server


# Error handling wrapper
def time_with_error_handling(stmt, setup, number=1):
    try:
        return timeit.timeit(stmt, setup, number=number)
    except Exception as e:
        print(f"An error occurred while timing {stmt}: {e}")
        return None


# Setup for ClientManager with enhanced Mocking
mock_sock = Mock()
mock_sock.recv.side_effect = [b'hello', b'world']  # More complex mocking
destination = 'destination_placeholder'
output_directory = 'output_dir_placeholder'
client_manager = ClientManager(mock_sock, destination, output_directory)

# Setup for ServerWizard
server_wizard = ServerWizard()

# Setup for Server
settings = Mock()
settings.port_number = 12345
settings.data_destination = 'destination_placeholder'
settings.output_dir = 'output_dir_placeholder'
server = Server(settings)


# ClientManager Timeits
def run_client_manager():
    client_manager.run()


def parse_client_manager():
    client_manager.parse_message()


timeit_client_manager_run = time_with_error_handling("run_client_manager()",
                                                     setup="from __main__ import run_client_manager", number=1000)
timeit_client_manager_parse = time_with_error_handling("parse_client_manager()",
                                                       setup="from __main__ import parse_client_manager", number=1000)


# ServerWizard Timeits
def ask_all_server_wizard():
    server_wizard.ask_all()


timeit_server_wizard_ask_all = time_with_error_handling("ask_all_server_wizard()",
                                                        setup="from __main__ import ask_all_server_wizard", number=1000)

# Server Timeits with limitations annotated
# Note: The listen function is not timed here due to its dependency on a real-world environment
# Uncomment if you decide to mock this function for timing.
# def listen_server():
#    server.listen()
# timeit_server_listen = time_with_error_handling("listen_server()", setup="from __main__ import listen_server", number=1000)

# Output the timing results
print(f"ClientManager.run() Time: {timeit_client_manager_run}")
print(f"ClientManager.parse_message() Time: {timeit_client_manager_parse}")
print(f"ServerWizard.ask_all() Time: {timeit_server_wizard_ask_all}")
# Uncomment if you decide to time the listen function
# print(f"Server.listen() Time: {timeit_server_listen}")
