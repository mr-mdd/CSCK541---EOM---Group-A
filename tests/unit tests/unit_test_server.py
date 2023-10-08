import unittest
from unittest.mock import Mock, patch
from src.server.client_manager import ClientManager
from src.server.server import Server
from src.server.server_wizard import ServerWizard, ServerSettings
from src.util.enums import ServerDestination, SecurityLevel, Source


class TestClientManager(unittest.TestCase):

    def setUp(self):
        # Setup common test environment for ClientManager tests
        self.sock = Mock()
        self.destination = ServerDestination.Print
        self.output_directory = 'output/'
        self.client_manager = ClientManager(self.sock, self.destination, self.output_directory)

    # Test the initialization of ClientManager attributes
    def test_init(self):
        self.assertEqual(self.client_manager.data_destination, ServerDestination.Print)
    
    # Test message parsing when it involves an initial message
    def test_parse_message_initial(self):
        self.client_manager.message = b'\x01\x02\x03'  # Mock initial message in bytes
        self.client_manager.parse_message()
        self.assertEqual(self.client_manager.data_source, 2)

        # Test message parsing when it contains payload data
    def test_parse_message_payload(self):
        self.client_manager.message = b'PayloadEND'
        self.client_manager.parse_message()
        self.assertEqual(self.client_manager.received_data, 'Payload')
    
    # Test data decryption when security level is set to 'Encrypted'
    def test_decrypt_data(self):
        self.client_manager.received_data = 'EncryptedData'
        self.client_manager.security_level = SecurityLevel.Encrypted.value
        self.client_manager.data_source = Source.TextFile.value  # Currently, it is only decrypting text files

        with patch.object(self.client_manager.crypt, 'decrypt', return_value='DecryptedData') as mock_decrypt:
            self.client_manager.decrypt_data()
            mock_decrypt.assert_called_once_with('EncryptedData')  # Ensure mock is called
            self.assertEqual(self.client_manager.decrypted_data, 'DecryptedData')
    
    # Test output method when data destination is set to 'Print'
    def test_output(self):
        self.client_manager.data_destination = ServerDestination.Print

        with patch('builtins.print') as mocked_print:
            self.client_manager.output()
            mocked_print.assert_called()


class TestServerWizard(unittest.TestCase):
    
    def setUp(self):
        # Setup common test environment for ServerWizard tests
        self.server_wizard = ServerWizard()
    
    # Test the initialization of ServerWizard attributes
    def test_init(self):
        self.assertIsInstance(self.server_wizard.get_server_settings(), ServerSettings)
    

class TestServer(unittest.TestCase):
    
    def setUp(self):
        # Setup common test environment for Server tests
        settings = Mock()
        settings.port_number = ('127.0.0.1', 5000)
        settings.data_destination = 'Print'
        settings.output_dir = 'output/'
        self.server = Server(settings)
    
    # Test the initialization of Server attributes
    def test_init(self):
        self.assertEqual(self.server.port_number, ('127.0.0.1', 5000))


if __name__ == '__main__':
    unittest.main()