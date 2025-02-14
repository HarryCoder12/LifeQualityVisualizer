import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
import os
import json

def parse_geojson(geojson_data, file_name):
    # Load GeoJSON into a GeoDataFrame
    
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    
    structured_data = gdf[["geometry"]].copy()
    structured_data["type"] = file_name.split(".")[0]
    # Before forloop
    for idx, rowData in structured_data.iterrows():
        # Check if the geometry is not a Point
        if rowData['geometry'].geom_type != "Point":
            if rowData['geometry'].geom_type == "LineString":
                # Convert the LineString to the first Point (or any specific point you prefer)
                # Here, I'm converting to the first coordinate of the LineString
                first_point = rowData['geometry'].coords[0]
                structured_data.at[idx, 'geometry'] = Point(first_point)
            else:
                # For any other type (e.g., Polygon), you could handle them similarly or just take a point from the geometry
                # For example, let's take the centroid of a Polygon
                structured_data.at[idx, 'geometry'] = rowData['geometry'].centroid

        # Print to verify the changes
        # print(structured_data.loc[idx, 'geometry'])
    print(structured_data)
    return structured_data

# Example usage
if __name__ == "__main__":
    directory_path = "exported-data"  # Replace with your directory path
    
    # Loop through all files in the directory
    for file_name in os.listdir(directory_path):
        # Check if the file ends with .geojson
        if file_name.endswith(".geojson"):
            file_path = os.path.join(directory_path, file_name)  # Get the full file path
            # Read GeoJSON file
            with open(file_path, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
            
            parsed_data = parse_geojson(geojson_data, file_name)
