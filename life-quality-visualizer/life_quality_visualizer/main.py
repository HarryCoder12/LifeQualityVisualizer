from point_rasterizer import generate_score_geojson
from shapely.geometry import Point
from scrap_OSM import get_data
from constants import PositionalConstants
import sys


if __name__ == "__main__":
    # setup parameters
    # source = Point(50.03972, 14.31167)  # left bottom corner
    _, size, x, y = sys.argv
    source = Point(float(x), float(y))
    fields = int(size) / 30
    constants = PositionalConstants(source, int(fields), 30, int(fields), 30)
    middle = constants.get_middle()
    distance = constants.get_max_distance()
    get_data(middle, distance)
    generate_score_geojson(constants)
