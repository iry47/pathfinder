import unittest
import sys


sys.path.insert(0, '/Users/ryanheadley/epitech/tor_2021_3') # change for your project path
from app.back.nlp.text_extract import extract_travel_request, get_geolocation
from geopy import Location

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
        
    def test_get_geolocation(self):
        result = get_geolocation('paris')
        expected = Location('Paris', 'Île-de-France', 'France métropolitaine', 'France', (48.8588897, 2.3200410217200766, 0.0))
        self.assertTrue(result == expected)