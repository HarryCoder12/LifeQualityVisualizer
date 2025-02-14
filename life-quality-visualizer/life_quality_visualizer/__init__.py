import osmnx as ox

# `True` means retrieve any object with this tag, regardless of value
# place = ", San Francisco, California"
# tags = {"building": True}
# gdf = ox.features.features_from_place(place, tags)
# gdf.shape

# dist = 1000
# address = "Prague 13"
# # features: https://wiki.openstreetmap.org/wiki/Map_features
tags = {"amenity": ["school"]}
#
# schools = ox.features.features_from_address(
#     address, tags, dist
# )  # geopandas GeoDataFrame
#
# # Export GeoDataFrame to file:
# schools.to_file("test")

# tags = {"amenity": True, "landuse": ["retail", "commercial"], "highway": "bus_stop"}
gdf = ox.features.features_from_place("Prague, Czechia", tags)
# gdf.shape
# print(gdf.to_json())
with open("exported-data/schools.geojson", "w") as f:
    f.write(gdf.to_json())
