import pandas as pd
import yaml

path_to_config = "../../config/main.yml"

class DataExtract:
    """
    All data provided by epitech
    """

    calendar_dates = None
    calendar = None
    routes = None
    stop_times = None
    stops = None
    transfers = None
    trips = None
    timetables = None

    def __init__(self, path_to_config):


        with open(path_to_config, 'r') as file:
            main_config = yaml.safe_load(file)

        self.calendar_dates = pd.read_csv(main_config["epitech_data"]["calendar_dates_path"])
        self.calendar = pd.read_csv(main_config["epitech_data"]["calendar_path"])
        self.routes = pd.read_csv(main_config["epitech_data"]["routes_path"])
        self.stop_times = pd.read_csv(main_config["epitech_data"]["stop_times_path"])
        self.stops = pd.read_csv(main_config["epitech_data"]["stops_path"])
        self.transfers = pd.read_csv(main_config["epitech_data"]["transfers_path"])
        self.trips = pd.read_csv(main_config["epitech_data"]["trips_path"])
        self.timetables = pd.read_table(main_config["epitech_data"]["timetable_path"])

    def get_routes(self, stop_id):
        """Get all routes passing through the station

        Args:
            stop_id (str): train station id in stops table
        """
        try:
            # sometimes stop_id are not in the stop_times
            stop_times_with_stop = self.stop_times[self.stop_times.stop_id == stop_id]
        except Exception as e:
            return e.message
        trips_with_stop_times = self.trips[self.trips.trip_id.isin(stop_times_with_stop.trip_id)]
        routes_with_trips = self.routes[self.routes.route_id.isin(trips_with_stop_times.route_id)]
        # print(routes_with_trips)

        return routes_with_trips

    def get_stations(self, route_id):
        """Get all station in a route

        Args:
            route_id (str): route id in routes tables
        """
        trips_with_route = self.trips[self.trips.route_id == route_id]
        stop_times_with_trips = self.stop_times[self.stop_times.trip_id.isin(trips_with_route.trip_id)]
        stops_with_stop_times = self.stops[self.stops.stop_id.isin(stop_times_with_trips.stop_id)]
        # print(stop_times_with_trips)

        return stops_with_stop_times