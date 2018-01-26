import unittest
from data_mining.handlers import db_connection_url, count_word_in_text, collect_urls_from

class TestHelpers(unittest.TestCase):

    def test_db_connection_url(self):
        self.assertEqual(db_connection_url('postgresql://localhost'), 'postgresql://localhost')
        self.assertFalse(db_connection_url())

    def test_count_word_in_text(self):
        text = 'Lorem ipsum dolor sit amet, an consectetur adipiscing elit, sed aN Do eiusmod tempor An incididunt ut labore et dolore magna aliqua'
        self.assertEqual(count_word_in_text(word='An', text=text), 3)
        self.assertEqual(count_word_in_text(word='loreM', text=text), 1)
        self.assertEqual(count_word_in_text(word='zzz', text=text), 0)
    
    def test_collect_urls_from(self):
        text_with_urls = "adadaaf http://az/cz jaad https://c.co af"
        self.assertEqual(collect_urls_from(text_with_urls), ['http://az/cz', 'https://c.co'])
        self.assertFalse(collect_urls_from("aaaa"))