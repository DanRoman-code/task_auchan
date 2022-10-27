import pickle
from unittest import TestCase

from data_extractor import DataExtractor

FILE_PATH = "test_data.data"


class TestDataExtractor(TestCase):
    def test_get_url_from_file(self):
        actual = DataExtractor().get_urls_from_file(FILE_PATH)
        self.assertEqual(actual, ["https://www.google.com/", "https://github.com/"])
