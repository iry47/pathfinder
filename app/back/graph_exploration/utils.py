import pandas as pd
import requests
from datetime import datetime, timedelta
import pickle

def get_duration_node_to_node(origin, dest):
    start_minute = int(origin.split(":")[1])
    start_hour = int(origin.split(":")[0])

    arrival_minute = int(dest.split(":")[1])
    arrival_hour = int(dest.split(":")[0])

    start_delta = timedelta(
        seconds=0,
        minutes=start_minute,
        hours=start_hour,
     )

    arrival_delta = timedelta(
        seconds=0,
        minutes=arrival_minute,
        hours=arrival_hour,
     )

    return arrival_delta - start_delta
