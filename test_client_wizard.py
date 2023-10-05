import unittest
from client_wizard import ClientWizard


class TestClientWizard(unittest.TestCase):
    """This test class is designed to validate the functional correctness and behavior of the methods within the ClientWizard class."""

    # Test the validation of IP addresses
    def test_is_valid_ip_address(self):
        client_wizard = ClientWizard()
        self.assertTrue(client_wizard.is_valid_ip_address('192.168.1.1'))
        self.assertFalse(client_wizard.is_valid_ip_address('300.300.300.300'))

    # Test the identification of valid and invalid port numbers
    def test_choose_port(self):
        client_wizard = ClientWizard()
        self.assertTrue(client_wizard._choose_port(80))
        self.assertFalse(client_wizard._choose_port(70000))

    # Test the setting of data source to either 'Dictionary' or 'TextFile'
    def test_choose_source(self):
        client_wizard = ClientWizard()
        self.assertEqual(client_wizard._choose_source('Dictionary'), 'Dictionary')
        self.assertEqual(client_wizard._choose_source('TextFile'), 'TextFile')

    # Test the setting of data format to either 'Binary', 'JSON', or 'XML'
    def test_choose_format(self):
        client_wizard = ClientWizard()
        self.assertEqual(client_wizard._choose_format('Binary'), 'Binary')
        self.assertEqual(client_wizard._choose_format('JSON'), 'JSON')

    # Test the setting of security level to either 'Encrypted' or 'UnEncrypted'
    def test_choose_security(self):
        client_wizard = ClientWizard()
        self.assertEqual(client_wizard._choose_security('Encrypted'), 'Encrypted')
        self.assertEqual(client_wizard._choose_security('UnEncrypted'), 'UnEncrypted')

    # Test if a dictionary is correctly built based on key-value pairs
    def test_build_dictionary(self):
        client_wizard = ClientWizard()
        test_dict = {'key1': 'value1', 'key2': 'value2'}
        self.assertEqual(client_wizard._build_dictionary(test_dict), test_dict)

    # Test if a text file is correctly built based on the content
    def test_build_textfile(self):
        client_wizard = ClientWizard()
        text_content = 'This is a sample text.'
        self.assertEqual(client_wizard._build_textfile(text_content), text_content)

    # Test the validation of file paths for text files
    def test_filepath_validation(self):
        client_wizard = ClientWizard()
        self.assertTrue(client_wizard._choose_textfile('/valid/path/to/textfile.txt'))
        self.assertFalse(client_wizard._choose_textfile('/invalid/path/:::.txt'))

    # Test the setting of file encryption
    def test_file_encryption_setting(self):
        client_wizard = ClientWizard()
        self.assertTrue(client_wizard._set_encryption(True))
        self.assertFalse(client_wizard._set_encryption(False))


if __name__ == '__main__':
    unittest.main()
