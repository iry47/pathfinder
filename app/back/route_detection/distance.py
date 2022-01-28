import pandas as pd
import mpu
from geopy.geocoders import Nominatim


def get_geo_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between to geographical points

    Args:
        lat_1 (float): first latitude
        long_1 (float): first longitude
        lat_2 (float): second latitude
        long_2 (float): second longitude
    """
    return mpu.haversine_distance((lat1, lon1), (lat2, lon2))


def get_geolocation(city):
    """Get the geolocation of a city

    Args:
        city (str): name of a city

    Returns:
        Array<geopy.location.Location>: Name, region, department, country, [lat, long, other]
    """
    geolocator = Nominatim(user_agent="travel_request")
    location = geolocator.geocode(city)
    return location


def get_closest_stations(cities):
    """
    Get closest train station for each cities passed
    Args:
        cities (dict): departure and destination

    Returns:
        dict: departure station and destination station
    """
    stops = pd.read_csv('../../../data/data_sncf/stops.txt') # TODO: fix path for application
    geo_departure = get_geolocation(cities["departure"])
    geo_destination = get_geolocation(cities["destination"])

    departure = {
        "current_lat": geo_departure.latitude,
        "current_lon": geo_departure.longitude,
        "stop": "",
        "distance": 99999
    }
    destination = {
        "current_lat": geo_destination.latitude,
        "current_lon": geo_destination.longitude,
        "stop": "",
        "distance": 99999
    }
    for index, row in stops.iterrows():
        distance_to_departure = get_geo_distance(
            departure["current_lat"],
            departure["current_lon"],
            row.stop_lat,
            row.stop_lon
        )
        print(distance_to_departure, departure["distance"])
        if distance_to_departure < departure["distance"]:
            departure["stop"] = row.stop_name
            departure["distance"] = distance_to_departure

        distance_to_destination = get_geo_distance(
            destination["current_lat"],
            destination["current_lon"],
            row.stop_lat,
            row.stop_lon
        )
        if distance_to_destination < destination["distance"]:
            destination["stop"] = row.stop_name
            destination["distance"] = distance_to_destination

    return departure["stop"], destination["stop"]