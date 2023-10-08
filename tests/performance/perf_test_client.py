import timeit
from unittest.mock import Mock
from src.client.client import Client
from src.client.client_wizard import ClientWizard

# Mock settings for Client
mock_settings = Mock()
mock_settings.hostname = 'localhost'
mock_settings.port_number = 8080


# Mock socket for Client
def mock_socket():
    mock = Mock()
    mock.connect = Mock(return_value=True)  # Simulate a successful connection
    return mock


# Function to test Client connection
def test_connect():
    client = Client(mock_settings)
    client._get_socket = mock_socket  # Override the method with our mock
    client.connect()


# Time the test_connect function
print(timeit.timeit("test_connect()", globals=globals(), number=10))


# Mock input for the ClientWizard
def mock_input(prompt):
    responses = {
        "Server: ": "localhost",
        "Number (1 - 65535): ": "8080",
    }
    return responses.get(prompt, "")


# Function to test ClientWizard
def test_client_wizard():
    wizard = ClientWizard()
    wizard._choose_host = mock_input  # Override the method with our mock
    wizard._choose_port = mock_input  # Override the method with our mock
    wizard.ask_all()


# Time the test_client_wizard function
print(timeit.timeit("test_client_wizard()", globals=globals(), number=10))
