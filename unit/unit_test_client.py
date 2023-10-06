import os 
import socket
import unittest
from unittest.mock import patch
from src.client.client import Client
from src.client.client_wizard import ClientWizard, ClientSettings

# Mocking the settings for testing
mock_settings = ClientSettings()
mock_settings.hostname = 'localhost'
mock_settings.port_number = 8080
mock_settings.source = 'Dictionary'
mock_settings.data_format = 'Binary'
mock_settings.dictionary = {'key': 'value'}
mock_settings.filepath = 'path/to/file'
mock_settings.security_level = 'UnEncrypted'


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(mock_settings)

    # Test if the socket is correctly initialized
    def test_get_socket(self):
        with patch('socket.socket') as mock_socket:
            self.client._get_socket()
            mock_socket.assert_called()

    # Test if the initial message is sent properly
    def test_send_initialisation_message(self):
        with patch('socket.socket.send') as mock_send:
            self.client.send_initialisation_message()
            mock_send.assert_called()

    # Test if the received message is parsed accurately
    def test_parse_message(self):
        self.client.message = b'ACK\0PublicKey\0'
        self.client.parse_message()
        self.assertEqual(self.client._public_key, 'PublicKey')

    # Test if the package is prepared as expected
    def test_prepare_package(self):
        self.client.prepare_package()
        self.assertIsNotNone(self.client._package_data)

    # Test if the payload is correctly sent through the socket
    def test_send_payload(self):
        with patch('socket.socket.send') as mock_send:
            self.client.prepare_package()
            self.client.send_payload()
            mock_send.assert_called()


class TestClientWizard(unittest.TestCase):
    def setUp(self):
        self.client_wizard = ClientWizard()

    # Test the validation of IP addresses
    def test_is_valid_ipaddress(self):
        self.assertTrue(self.client_wizard.is_valid_ipaddress('192.168.1.1'))
        self.assertFalse(self.client_wizard.is_valid_ipaddress('invalid'))

    # Test the port number selection
    def test_choose_port(self):
        with patch('builtins.input', return_value='8080'):
            self.client_wizard._choose_port()
            self.assertEqual(self.client_wizard._settings.port_number, 8080)

    # Test the data source selection functionality
    def test_choose_source(self):
        with patch('builtins.input', return_value='d'):
            self.client_wizard._choose_source()
            self.assertEqual(self.client_wizard._settings.source, 'Dictionary')

    # Test the security level selection
    def test_choose_security(self):
        with patch('builtins.input', return_value='n'):
            self.client_wizard._choose_security()
            self.assertEqual(self.client_wizard._settings.security_level, 'UnEncrypted')

    # Test the construction of the data dictionary
    def test_build_dictionary(self):
        with patch('builtins.input', side_effect=['key', 'value', 'x']):
            self.client_wizard._build_dictionary()
            self.assertEqual(self.client_wizard._settings.dictionary, {'key': 'value'})


if __name__ == '__main__':
    unittest.main()
