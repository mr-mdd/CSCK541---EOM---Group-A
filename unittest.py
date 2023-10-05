import os 
from branston import Branston
import socket
from enums import *
from crypt import Crypt
from cwizard import ClientWizard
import unittest
import timeit

# Unit testing framework 
class UnitTest(unittest.TestCase):

    # Test 1: To confirm the creation of a new dictionary from cwizard.py
    def test_build_dictionary(self):
        friend_name = ["Mary", "Tom", "Sally"]
        friend_height = [160, 170, 180]
        # Test the function of the build_dictionary
        data_str = build_dictionary(friend_name, friend_height)
        actual = data_str
        expected = {'Mary': 160, 'Tom': 170, 'Sally': 180}
        # Check whether the expected is equal to the actual
        self.assertEqual(actual, expected)
        print("unittest: test_build_dictionary is passed")
    
    # Test 2: To confirm...

    if __name__ == '__main__':
        unittest.main()

# Performance test to verify the application on the speed
