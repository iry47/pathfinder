# -*- coding: utf-8 -*-
import unittest
import mpu

from app.back.route_detection.distance import get_geo_distance
from app.back.route_detection.distance import get_closest_stations


class TestRouteDetection(unittest.TestCase):

    """class for running unittests."""

    def setUp(self):
        """Your setUp"""
        self.test_lat1 = 52.2296756
        self.test_lon1 = 21.0122287
        self.test_lat2 = 52.406374
        self.test_lon2 = 16.9251681

    def test_get_geo_distance(self):
        geo_distance = get_geo_distance(
            52.2296756,
            21.0122287,
            52.406374,
            16.9251681
        )

        self.assertEqual(geo_distance, 278.45817507541943)

    def test_get_closest_stations(self):
        result = get_closest_stations({
            'departure': 'paris',
            'destination': 'lyon'
        })

        expected = ('Gare de Paris-Montparnasse 1-2', 'Lyon-St-Paul-la-Feuilée')

        self.assertEqual(result, expected)
