import unittest

from app.back.data_extract import DataExtract, path_to_config

class TestDataExtract(unittest.TestCase):
    """
    Test all functions related to extracting data
    from epitech dataset
    """

    data = None
    test_stop_id = ""
    test_route_id = ""


    def setUp(self):
        path_to_config = "../../../config/main.yml"
        self.data = DataExtract(path_to_config)
        self.test_stop_id = "StopPoint:OCECar TER-87381509"
        self.test_route_id = "OCE1506035"

    def test_get_routes(self):
        routes = self.data.get_routes(self.test_stop_id)

        self.assertEqual(routes.shape, (2,9))

    def test_get_stations(self):
        stations = self.data.get_stations(self.test_route_id)

        self.assertEqual(stations.shape, (21, 9))

