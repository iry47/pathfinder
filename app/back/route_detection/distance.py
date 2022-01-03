import mpu

def get_geo_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between to geographical points

    Args:
        lat_1 (float): first latitude
        long_1 (float): first longitude
        lat_2 (float): second latitude
        long_2 (float): second longitude
    """
    return mpu.haversine_distance((lat1, lon1), (lat2, lon2))