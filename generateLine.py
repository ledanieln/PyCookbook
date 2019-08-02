import pandas as pd
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
import pyproj

# Input/Output file paths go here
inputPath = '../data/processed/BFT_MISSIONS_20190724.csv'
outputPath = '../data/processed/missionLines.shp'

data = pd.read_csv(inputPath)

# Take just the necessary fields
sData = pd.concat([data['ReportId'], data['Longitude'], data['Latitude'], data['Mission Number']], axis=1)

# Create geometry from latitude/longitude
geometry = [Point(xy) for xy in zip(sData.Longitude, sData.Latitude)]
sData['geometry'] = geometry

# Segment data by mission number/segment number, whatever is preferred
#and connect the points in order 
segmentData = sData.sort_values('ReportDate').groupby(['Mission Number'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size> 1 else None)

# Combine data into GeoDataFrame
finalData = finalData = GeoDataFrame(segmentData, geometry='geometry').reset_index()

# Set coordinate system
finalData.crs = {'init': 'epsg:4326'}

# Export Data
finalData.to_file(outputPath)