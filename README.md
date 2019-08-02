# PyCookbook
Scripts I've written for data processing use and portfolio purposes. Some of these scripts are specific to certain projects so they may need to be generalized for different purposes.

# Descriptions
These are descriptions of each file in the cook book along with the required packages.

**generateLine.py** *(pandas, geoPandas, numPy, Shapely)*  
Generates spatial trajectory lines from temporally sequential geospatial point data. 

**rasterProcessing.py** *(GDAL, shapely, numpy)*  
Converting JPEG2000 rasters into JPEG rasters using GDAL  
Resampling raster according to multiplier  
Generating boundary vectors according to image boundary  

**vectorProcessing.py** *(subprocess, fiona, glob, time, os, shapely, json)*  
Clipping polygons by vector boundary  
Converting GeoJSON into COCO format for Mask-RCNN  
