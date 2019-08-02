import pandas as pd
import numpy as np
import time
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString

data = pd.read_csv('../data/raw/output_preds1.csv')

#unique ID of Tail Number and Mission Date
data['uniqueID'] = data['TailNumber'] + '/' + data['Mission Date'].map(lambda x: x.split(' ')[0])

# Zip the coordinates into a point object and convert to a GeoDataFrame
geometry = [Point(xy) for xy in zip(data.Longitude, data.Latitude)]
pointData = GeoDataFrame(data, geometry=geometry)

# def toDatetime(string):
#     return time.strptime(string.split(' ')[0], '%Y-%M-%d')

#Aggregate points with groupby
missionData = data.groupby(['uniqueID'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else None)
#missionData = data.groupby(['Mission Number'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else None)
#missionData = data.groupby(['Mission Number'])['Tail Number'].apply(lambda x: LineString(x.tolist()))

missionNumber = data.groupby(['uniqueID'])

finalData = GeoDataFrame(missionData, geometry='geometry')

data.to_csv('../data/processed/output_preds_2.csv')

with open('../data/processed/missionLinesUpdate.geojson', 'w') as f:
    f.write(finalData.to_json())

#finalData.to_file('../data/processed/missionLinesUpdate.shp')

# list = data['Mission Number'].unique()
#
# # print('Number of Missions')
# # print(len(list))
# # print(list)
# #
# # print(data.columns)
#
# # missionDF = data.loc[data['Mission Number'] == list[0]]
# # missionLat = missionDF['Latitude']
# # missionLong = missionDF['Longitude']
# # mission = missionDF['Mission Number']
# #
# # pos = pd.concat([missionLat, missionLong, mission], axis=1)
# # print(pos)
#
# newData = data.assign(nextLat=data.groupby('Mission Number').Latitude.shift(-1), nextLong=data.groupby('Mission Number').Longitude.shift(-1))
#
# onlyPos = pd.concat([newData['Mission Number'], newData['Latitude'], newData['Longitude'], newData['nextLat'], newData['nextLong']], axis=1)
#
# onlyPos.to_csv('../data/processed/positions.csv')
