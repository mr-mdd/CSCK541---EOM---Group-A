import unittest
from src.util.branston import Branston, Format
from src.util.crypt import Crypt
from src.util.enums import Format, Source, SecurityLevel, ServerDestination
import rsa


class TestBranston(unittest.TestCase):

    # Tests the default initialization of the Branston class
    def test_initialization(self):
        branston = Branston()
        self.assertEqual(branston.get_pickling_format(), Format.BINARY)

    # Tests the ability to set a different pickling format
    def test_set_pickling_format(self):
        branston = Branston()
        branston.set_pickling_format(Format.JSON.value)
        self.assertEqual(branston.get_pickling_format(), Format.JSON.value)

    # Tests the exception raised when setting an invalid pickling format
    def test_invalid_pickling_format(self):
        branston = Branston()
        with self.assertRaises(Exception):
            branston.set_pickling_format("INVALID")

    # Tests the pickling and unpickling of data in binary format
    def test_pickle_binary(self):
        branston = Branston()
        data = {"key": "value"}
        pickled_data = branston.pickle(data)
        unpickled_data = branston.unpickle(pickled_data)
        self.assertEqual(data, unpickled_data)

    # Tests the pickling and unpickling of data in JSON format
    def test_pickle_json(self):
        branston = Branston()
        branston.set_pickling_format(Format.JSON.value)
        data = {"key": "value"}
        pickled_data = branston.pickle(data)
        unpickled_data = branston.unpickle(pickled_data)
        self.assertEqual(data, unpickled_data)


class TestCrypt(unittest.TestCase):

    # Tests the initialization of the Crypt class with new keys
    def test_new_keys(self):
        crypt = Crypt.new_keys()
        self.assertIsNotNone(crypt.get_public_key())

    # Tests the initialization of the Crypt class with a provided public key
    def test_with_key(self):
        public_key = rsa.PublicKey(65537, 9990454943)
        crypt = Crypt.with_key(public_key)
        self.assertEqual(crypt.get_public_key(), public_key)

    # Tests the ability to encrypt and then decrypt a string
    def test_encrypt_decrypt(self):
        crypt = Crypt.new_keys()
        data = "Hello, World!"
        encrypted_data = crypt.encrypt(data)
        decrypted_data = crypt.decrypt(encrypted_data)
        self.assertEqual(data, decrypted_data)

    # Tests that an exception is raised when no private key is available for decryption
    def test_no_private_key(self):
        public_key = rsa.PublicKey(65537, 9990454943)
        crypt = Crypt.with_key(public_key)
        with self.assertRaises(Exception):
            crypt.decrypt("some_data")

    # Tests that the getter method for the public key returns an instance of rsa.PublicKey
    def test_get_public_key(self):
        crypt = Crypt.new_keys()
        self.assertIsInstance(crypt.get_public_key(), rsa.PublicKey)


class TestEnums(unittest.TestCase):

    # Tests that the Format enum has the correct value for BINARY
    def test_format_enum(self):
        self.assertEqual(Format.BINARY.value, 1)

    # Tests that the Source enum has the correct value for Dictionary
    def test_source_enum(self):
        self.assertEqual(Source.Dictionary.value, 4)

    # Tests that the SecurityLevel enum has the correct value for UnEncrypted
    def test_security_level_enum(self):
        self.assertEqual(SecurityLevel.Plain.value, 16)

    # Tests that the ServerDestination enum has the correct value for Print
    def test_server_destination_enum(self):
        self.assertEqual(ServerDestination.Print.value, 512)


if __name__ == "__main__":
    unittest.main()
