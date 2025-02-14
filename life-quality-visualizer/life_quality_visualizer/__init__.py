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
            "tags": {"building": ["sports_centre", "stadium", "sports_hall"]},
        },
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
