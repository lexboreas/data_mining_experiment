import unittest
from data_mining.myqueue import custom_decode, custom_encode

class TestMyQueue(unittest.TestCase):

    def test_custom_encode_and_decode_for_string(self):
        some_text = "Test message"
        self.assertEqual(custom_decode(custom_encode(some_text)), some_text)
        self.assertNotEqual(custom_encode(some_text), some_text)

    def test_custom_encode_and_decode_for_dictionary(self):
        some_dictionary = {'name': 'test', 'body': 'some body'}
        self.assertEqual(custom_decode(custom_encode(some_dictionary)), some_dictionary)

