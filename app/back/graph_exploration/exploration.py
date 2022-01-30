import pandas as pd
import requests
from datetime import datetime
from datetime import timedelta
import pickle

from .utils import get_duration_node_to_node

def load_cities():
    f = open("./../data/cities.pkl", "rb")
    cities = pickle.load(f)
    f.close()

    if not cities:
        stops = pd.read_csv('./../data/data_sncf/stops.csv', sep=",")
        stops = stops[stops['stop_id'].str.contains('StopPoint:OCETrain')]
        stops = stops.set_index('stop_id').T.to_dict()
        cities = {}

        for city in list(stops.items()):
            cities.update({
                city[0]: {
                    "stop_name": city[1]["stop_name"],
                    "coord": [city[1]["stop_lat"], city[1]["stop_lon"]],
            }})
    return cities

def load_trips():
    f = open("./../data/trips.pkl", "rb")
    trips_tmp = pickle.load(f)
    f.close()

    if trips_tmp is None:
        stop_times = pd.read_csv('./../data/data_sncf/stop_times.csv', sep=",")
        trips = pd.read_csv('./../data/data_sncf/trips.csv', sep=",")

        stop_times = stop_times[stop_times['stop_id'].str.contains('StopPoint:OCETrain')]

        trips = trips.drop(labels=["service_id", "block_id", "shape_id", "trip_headsign"], axis=1)

        trips = trips.set_index('trip_id').T.to_dict()

        trips_tmp = {}
        for trip in list(trips.items()):
            trips_tmp.update({trip[0]:{"nodes": []}})
            selected_stop_times = stop_times.loc[stop_times['trip_id'] == trip[0]]
            for trip_tmp in selected_stop_times.iterrows():
                trips_tmp[trip[0]]["nodes"].append({"trip_id": trip[0], "stop_id": trip_tmp[1]["stop_id"],"arrival_time": trip_tmp[1]["arrival_time"]})
    return trips_tmp

def load_graph():
    f = open("./../data/graph.pkl", "rb")
    routes_graph = pickle.load(f)
    f.close()

    trips_tmp = load_trips()
    cities = load_cities()

    if routes_graph:
        routes_graph = {}
        for route in list(trips_tmp.items()):
            for i in range (0, len(route[1]["nodes"])):
                city_id = route[1]["nodes"][i]["stop_id"]
                city = cities[city_id]
                if city_id not in routes_graph:
                    routes_graph.update({city_id: []})
                    if i != 0:
                        routes_graph[city_id].append({route[1]["nodes"][i - 1]["stop_id"]: get_duration_node_to_node(route[1]["nodes"][i - 1]["arrival_time"], route[1]["nodes"][i]["arrival_time"])})
                    if i != len(route[1]["nodes"]) - 1:
                        routes_graph[city_id].append({route[1]["nodes"][i + 1]["stop_id"]: get_duration_node_to_node(route[1]["nodes"][i]["arrival_time"], route[1]["nodes"][i + 1]["arrival_time"])})
                elif route[1]["nodes"][i - 1]["stop_id"] not in routes_graph[city_id] and i != 0:
                    routes_graph[city_id].append({route[1]["nodes"][i - 1]["stop_id"]: get_duration_node_to_node(route[1]["nodes"][i - 1]["arrival_time"], route[1]["nodes"][i]["arrival_time"])})
                elif i < len(route[1]["nodes"]) - 1 and route[1]["nodes"][i + 1]["stop_id"] not in routes_graph[city_id]:
                    routes_graph[city_id].append({route[1]["nodes"][i + 1]["stop_id"]: get_duration_node_to_node(route[1]["nodes"][i]["arrival_time"], route[1]["nodes"][i + 1]["arrival_time"])})
    return routes_graph


def convert_route_to_cities(route):
    cities = load_cities()
    route_cities = []
    # for route in routes:
    for city in route["route"]:
        route_cities.append(cities[list(city)[0]]["stop_name"])
    return route_cities


def convert_city_to_stop_points(city):
    stops_tmp = pd.read_csv('../data/data_sncf/stops.csv', sep=",")
    stops_tmp = stops_tmp[stops_tmp['stop_id'].str.contains('StopPoint:OCETrain')]
    stops_tmp = stops_tmp[stops_tmp['stop_name'].str.contains(city)]
    stop_points = []
    for stop in stops_tmp.iterrows():
        stop_points.append({stop[1]["stop_id"]: timedelta(hours=0)})
    return stop_points



def graph_exploration(graph, start, goal):
    cities = load_cities()

    explored = []
    queue = [[start]]
    if start == goal:
        return
    valide_routes = []
    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored and node != goal:
            node_id = list(node.keys())[0]
            neighbours = graph[node_id]
            duration = timedelta(hours=0)
            for neighbour in neighbours:
                if list(neighbour)[0] in cities:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    duration = duration + neighbour[list(neighbour)[0]]
                    if list(neighbour)[0] == list(goal)[0]:
                        if len(valide_routes) > 25:
                            return valide_routes
                        valide_routes.append({"route": new_path, "duration": duration})
            explored.append(node)
    return valide_routes
