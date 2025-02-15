import osmnx as ox


def get_feature(place, tags):
    # features: https://wiki.openstreetmap.org/wiki/Map_features
    return ox.features.features_from_place(place, tags)


def get_features(place="Prague, Czechia"):
    features = [
        {
            "name": "schools",
            "tags": {"amenity": ["school"]},
        },
        {
            "name": "sports",
            "tags": {
                "building": ["sports_centre", "stadium", "sports_hall"],
                "leisure": [
                    "fitness_center",
                    "fitness_station",
                    "sports_hall",
                    "stadium",
                    "swimming_pool",
                    "swimming_area",
                    "track",
                    "ice_rink",
                    "dog_park",
                    "disc_golf_course",
                ],
            },
        },
        {
            "name": "greenAreas",
            "tags": {
                "landuse": ["forest"],
                "leisure": ["park"],
            },
        },
        {
            "name": "publicTransport",
            "tags": {
                "amenity": ["bus_station", "ferry_terminal", "train_station"],
                "highway": ["bus_stop"],
                "public_transport": ["station"],
            },
        },
        {
            "name": "shops",
            "tags": {
                "shop": [
                    "convenience",
                    "supermarket",
                    "bakery",
                    "butcher",
                    "food",
                    "general",
                ]
            },
        },
        {
            "name": "healthcare",
            "tags": {
                "amenity": ["clinic", "hospital", "pharmacy"],
                "healthcare": ["centre", "physiotherapist", "psychotherapist", "rehabilitation"],
            },
        },
        {
            "name": "restaurants",
            "tags": {
                "amenity": ["bar", "cafe", "fast_food", "pub", "restaurant"],
            },
        },
        # {
        #     "name": "noise",
        #     "tags": {
        #         "highway": ["motorway", "trunk", "primary"],
        #     }
        # }
        #TODO: urady, 
    ]

    for feature in features:
        feature["gdf"] = get_feature(place, feature["tags"])
    return features


def write_geojson(gdf_name):
    for feature in gdf_name:
        with open(
            f"exported-data/{feature["name"]}.geojson", "w", encoding="UTF-8"
        ) as f:
            f.write(feature["gdf"].to_json())


if __name__ == "__main__":
    write_geojson(get_features())
