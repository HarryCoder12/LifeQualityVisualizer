import geopandas
from geopandas import GeoDataFrame
from math import radians, cos, sin, asin, sqrt
from dataclasses import dataclass
from data_processing import get_sanitezed_data


@dataclass
class Point:
    x: float
    y: float


@dataclass
class ClusterQuality:
    public_transport: bool
    school: bool
    green_area: bool
    health_care: bool
    sport_facility: bool
    shop: bool
    restaurant: bool
    x: float
    y: float

    def add_type(self, str_type, p):
        self.x = p.x  # take last geo coordinates
        self.y = p.y
        if str_type == "publicTransport":
            self.public_transport = True
        elif str_type == "schools":
            self.school = True
        elif str_type == "greenAreas":
            self.green_area = True
        elif str_type == "healthcare":
            self.health_care = True
        elif str_type == "sports":
            self.sport_facility = True
        elif str_type == "shops":
            self.shop = True
        elif str_type == "restaurants":
            self.restaurant = True
        else:
            print(str_type)
            raise Exception("Unknown type")

    def has_data(self):
        return (
            self.public_transport
            or self.school
            or self.green_area
            or self.health_care
            or self.sport_facility
            or self.restaurant
        )

@dataclass
class GridClass:
    public_transport: float = 0.0
    school: float = 0.0
    green_area: float = 0.0
    health_care: float = 0.0
    sport_facility: float = 0.0
    shop: float = 0.0
    restaurant: float = 0.0
    x: float = 0.0
    y: float = 0.0


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SIZE = 1000  # grid size
ONE_METER_X = 0.00001425
FIELD_SIZE_X = ONE_METER_X * 10
SIZE_X = 1000  # cells count each FIELD_SIZE_X width
WIDTH_X = FIELD_SIZE_X * SIZE_X

ONE_METER_Y = 0.000008989
FIELD_SIZE_Y = ONE_METER_Y * 10
SIZE_Y = 100  # cells count each FIELD_SIZE_Y height
HEIGHT_Y = FIELD_SIZE_Y * SIZE_Y

# SOURCE = Point(50.054153, 14.347182)
# SOURCE = Point(14.445755, 50.085048)
SOURCE = Point(14.443862, 50.085356)
point_counter = 0

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


def place_in_cluster(cluster_map, point, type, source, width, height):
    global point_counter
    if point.geom_type != "Point":
        return
    if not is_in_area(point, source, width, height):
        return

    point_counter += 1
    x, y = convert_to_cluster_index(point, source)
    cluster_map[x][y].add_type(type, point)


def convert_to_cluster_index(point, source):
    x = int((point.x - source.x) / FIELD_SIZE_X)
    y = int((point.y - source.y) / FIELD_SIZE_Y)
    return x, y


if __name__ == "__main__":
    cluster_map = [
        [
            ClusterQuality(
                False, False, False, False, False, False, False, False, 0.0, 0.0
            )
            for _ in range(SIZE_Y)
        ]
        for _ in range(SIZE_X)
    ]
    grid_map = [[GridClass(x=i, y=j) for j in range(SIZE)] for i in range(SIZE)]
    # sanitized_data = geopandas.read_file("sanitized-data/everything.geojson")
    # print(sanitized_data)
    for index, row in get_sanitezed_data().iterrows():
        point = row["geometry"]
        type = row["type"]
        place_in_cluster(cluster_map, point, type, SOURCE, WIDTH_X, HEIGHT_Y)
    # print(cluster_map)

    for rowIndex, row in enumerate(cluster_map):
        for colIndex, cell in enumerate(row):
            if cell.has_data():
                grid_map[rowIndex][colIndex] = GridClass()
    print(
        f"diagonal length: {
        haversine(SOURCE.x, SOURCE.y, SOURCE.x + WIDTH_X, SOURCE.y + HEIGHT_Y)}"
    )  # size of diagonal
    print(f"point count: {point_counter}")

                

