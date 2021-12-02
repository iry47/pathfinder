import unittest
from app.back.text_extract import extract_travel_request

class TextExtractTests(unittest.TestCase):

    """class for running unittests."""

    def setUp(self):
        """Your setUp"""
        self.sentences = [
            'Voyager en train de lille à lyon',
            'Les trains sont mieux. J\'irai de Lille à Lyon',
            'A toulon et prendre un bus à marseille',
            'A toulon et prendre un avion à marseille',
            'A toulon et marcher à marseille',
            'Manger des fruits',
            'Nager a la plage'    
        ]

    def test_extract_travel_info(self):
        result = extract_travel_request(self.sentences)
        expected = {
            "departure": "Lille",
            "destination": "Lyon"
        }
        print(result)
        self.assertTrue(result == expected)