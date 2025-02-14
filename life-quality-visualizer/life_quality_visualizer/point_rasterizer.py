import geopandas
from geopandas import GeoDataFrame
from math import radians, cos, sin, asin, sqrt
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class ClusterQuality:
    subway: bool
    other_public_transport: bool
    school: bool
    green_area: bool
    health_care: bool
    sport_facility: bool


SIZE = 100
ONE_METER_X = 0.00001425
WIDTH_X = ONE_METER_X * SIZE
ONE_METER_Y = 0.000008989
HEIGHT_Y = ONE_METER_Y * SIZE
SOURCE = Point(50.054153,14.347182)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)

    source: https://stackoverflow.com/a/4913653
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r * 1000  # return in meters


def is_in_area(point, source, width, height):
    if (
        source.x <= point.x <= source.x + width
        and source.y <= point.y <= source.y + height
    ):
        return True
    return False


def place_in_cluster(cluster_map, point, source, width, height):
    #if isinstance(point, geopandas.shapely.geome):
    if point.geom_type != "Point":
        return
    if not is_in_area(point, source, width, height):
        return

    x, y = convert_to_cluster_index(point, source)
    cluster_map[x][y] = 1  # TODO: put valid value here


def convert_to_cluster_index(point, source):
    x = (int((point.x - source.x) / ONE_METER_X),)
    y = int((point.y - source.y) / ONE_METER_Y)
    return x, y


if __name__ == "__main__":
    cluster_map = [
        [ClusterQuality(False, False, False, False, False, False) for _ in range(SIZE)]
        for _ in range(SIZE)
    ]

    gdf = geopandas.read_file("exported-data/schools.geojson")
    for point in gdf["geometry"]:
        place_in_cluster(cluster_map, point, SOURCE, WIDTH_X, HEIGHT_Y)
    print(cluster_map)
