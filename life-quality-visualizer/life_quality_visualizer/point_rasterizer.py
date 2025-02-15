import geopandas
from geopandas import GeoDataFrame
from math import radians, cos, sin, asin, sqrt
from dataclasses import dataclass
from data_processing import get_sanitezed_data
from shapely.geometry import Point
import constants


@dataclass
class ClusterQuality:
    # ordering: public_transport, school, green_area, health_care, sport_facility, shop, restaurant
    features: list[bool, bool, bool, bool, bool, bool, bool]
    x: float
    y: float
    valid: bool

    def __init__(self, x, y):
        self.features = [False, False, False, False, False, False, False]
        self.x = x
        self.y = y

    def add_type(self, str_type, p):
        # self.x = p.x  # take last geo coordinates
        # self.y = p.y
        names = [
            "publicTransport",
            "schools",
            "greenAreas",
            "healthcare",
            "sports",
            "shops",
            "restaurants",
        ]
        i = names.index(str_type)
        if i >= 0:
            self.features[i] = True

    def has_data(self):
        for feature in self.features:
            if feature:
                return True
        return False


@dataclass
class GridClass:
    feature_scores: list[int, int, int, int, int, int, int, int]
    x: float
    y: float

    def __init__(self):
        self.feature_scores = [0, 0, 0, 0, 0, 0, 0, 0]
        self.x = 0
        self.y = 0

    def has_score(self):
        for score in self.feature_scores:
            if score > 0:
                return True
        return False

        
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


def place_in_cluster(cluster_map, point, type, constants):
    if point.geom_type != "Point":
        return
    if not is_in_area(point, constants.SOURCE, constants.WIDTH_X, constants.HEIGHT_Y):
        return

    x, y = convert_to_cluster_index(point, constants.SOURCE, constants)
    cluster_map[x][y].add_type(type, point)


def convert_to_cluster_index(point, source, constants):
    x = int((point.x - source.x) / constants.FIELD_SIZE_X)
    y = int((point.y - source.y) / constants.FIELD_SIZE_Y)
    return x, y


def get_score_map(c_map, constants):
    score_map = [[GridClass() for _ in range(constants.SIZE_Y)] for _ in range(constants.SIZE_X)]
    for rowIndex, row in enumerate(c_map):
        for colIndex, cell in enumerate(row):
            if cell.has_data():
                propagate_score(score_map, rowIndex, colIndex, cell, constants)
            score_map[rowIndex][colIndex].x = c_map[rowIndex][colIndex].x
            score_map[rowIndex][colIndex].y = c_map[rowIndex][colIndex].y
    return score_map


def propagate_score(score_map, rowIndex, colIndex, cell, constants):
    INFLUENCE_RADIUS = 12
    for i in range(-INFLUENCE_RADIUS, INFLUENCE_RADIUS):
        for j in range(-INFLUENCE_RADIUS, INFLUENCE_RADIUS):
            x = rowIndex + i
            y = colIndex + j
            if is_coord_valid(x, y, constants):
                distance = sqrt(((i) ** 2) + ((j) ** 2))
                if distance == 0:# or distance > INFLUENCE_RADIUS:  # do not influence the cell itself or cells that are too far
                    return
                for feature_index, feature in enumerate(cell.features):
                    if feature:
                        current = score_map[x][y].feature_scores[feature_index]
                        score_map[x][y].feature_scores[feature_index] = max(
                            current, 1000 - constants.FIELD_DIAGONAL * distance
                        )  # idk if 1000 is good constant


def convert_score_map_to_geo_json(score_map):
    features = []
    geometry = []
    for row in score_map:
        for cell in row:
            if cell.has_score():
                features.append(cell.feature_scores)
                geometry.append(Point(cell.x, cell.y))
    gdf = GeoDataFrame({"geometry": geometry, "feature": features}, crs="EPSG:4326")
    return gdf


def is_coord_valid(x, y, constants):
    return 0 <= x < constants.SIZE_X and 0 <= y < constants.SIZE_Y


def generate_score_geojson(constants):
    cluster_map = [
        [
            ClusterQuality(constants.SOURCE.x + x * constants.FIELD_SIZE_X, constants.SOURCE.y + y * constants.FIELD_SIZE_Y)
            for y in range(constants.SIZE_Y)
        ]
        for x in range(constants.SIZE_X)
    ]

    # sanitized_data = geopandas.read_file("sanitized-data/everything.geojson")
    # print(sanitized_data)
    for index, row in get_sanitezed_data().iterrows():
        point = row["geometry"]
        type = row["type"]
        place_in_cluster(cluster_map, point, type, constants)
    # print(cluster_map)

    score_map = get_score_map(cluster_map, constants)
    gdf = convert_score_map_to_geo_json(score_map)
    with open("sanitized-data/lifeQuality.geojson", "w", encoding="UTF-8") as f:
        f.write(gdf.to_json())

    # print(
    #     f"diagonal length: {haversine(SOURCE.x, SOURCE.y, SOURCE.x + WIDTH_X, SOURCE.y + HEIGHT_Y)}"
    # )  # size of diagonal

if __name__ == "__main__":
    constants = constants.PositionalConstants(Point(50.03972, 14.31167), 100, 30, 100, 30)
    generate_score_geojson(constants)