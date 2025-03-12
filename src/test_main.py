import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = '# Hello'
        self.assertEqual('Hello', extract_title(md))

    def test_multiline_extract_title(self):
        md = '''# Hello
        this is the body text
        '''
        self.assertEqual('Hello', extract_title(md))