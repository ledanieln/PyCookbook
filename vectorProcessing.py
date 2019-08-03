import subprocess
import fiona
import time
import rasterProcessing as rp
import os
import json
import math
from osgeo import gdal, osr, ogr
from collections import OrderedDict

# indexStr = glob.glob('../data/interim/2017/*.shp')
# clip_src = indexStr[1]
# print(indexStr)

def clipPolygonByRaster(src_raster, dstPath, gdbPath, gdbTable):
    #Get boundaries for polygons
    clip_src = rp.generateBoundaryIndex(src_raster)
    xmin = str(clip_src[0])
    ymin = str(clip_src[1])
    xmax = str(clip_src[2])
    ymax = str(clip_src[3])

    attributesSaved = 'SOURCE, FEATURE, SHAPE_AREA'

    outFileName = dstPath + os.path.basename(src_raster).split('.')[0] + ".geojson"

    #print("Beginning Clip")
    start = time.clock()

    p = subprocess.call(["/usr/bin/ogr2ogr", "-f", "GeoJSON", "-select", attributesSaved, "-spat", xmin, ymin, xmax, ymax, "-clipsrc", "spat_extent", outFileName, gdbPath, gdbTable], shell=False)
    #p.kill()
    #print('Clipped in %.5f seconds' % (time.clock()-start))

    #Project Vector


#Test:
clipPolygonByRaster('/data/COA Aerial Data/2012/JP2/AUSTIN_EAST-NEA1.jp2', '../data/interim/test/', '../data/raw/TX_STATE_DATA.gdb', 'planimetrics_2013')

def findCategoryID(categoryStr):
    with open('../references/categories-all.json', 'r') as json_file:
        categories = json.load(json_file)
        for item in categories:
             if categoryStr == item['name']:
                 return item['id']

def geoJSONtoCOCO(src_raster, srcGeoJSON, imageNum, prevNum):
    clip_src = rp.generateBoundaryIndex(src_raster)
    xOrigin = clip_src[0]
    yOrigin = clip_src[1]
    width = clip_src[4]
    height = clip_src[5]

    fileName = os.path.basename(src_raster).split('.')[0]

    newShapeList = []
    #IMPORTANT NOTE: This algorithm removes multipolygons. These are shape files with multiple polygons in them. The ID will be different than the original dataset.
    with fiona.open(srcGeoJSON) as shapes:
        overX = 0
        overY = 0
        negZeroCounter = 0
        for shape in shapes:
            if shape['geometry']['type'] == 'Polygon':
                newShape = OrderedDict()
                newShape['id'] = prevNum
                newShape['image_id'] = imageNum
                newShape['category_id'] = findCategoryID(str(shape['properties']['FEATURE']))

                newPolygon = []
                newSegmentation = []
                Xarr = []
                Yarr = []

                for coordPair in shape['geometry']['coordinates'][0]:
                    #newCoordPair = []
                    #print("coord pair")
                    #print(coordPair[0], coordPair[1])
                    X = (coordPair[0] - xOrigin)
                    Y = -1 * (coordPair[1] - yOrigin)
                    #newCoordPair.append(X)
                    #newCoordPair.append(Y)
                    #print("X & Y")
                    #print(2*X, 2*Y)

                    if(X == -0):
                        negZeroCounter = negZeroCounter + 1
                        X = 0
                    if(Y == -0):
                        negZeroCounter = negZeroCounter + 1
                        Y = 0

                    if(math.floor(2*X) > width-1):
                        overX = overX + 1
                        newPolygon.append(width-1)
                        Xarr.append(2*X)
                    else:
                        newPolygon.append(math.floor(2*X))
                        Xarr.append(2*X)

                    if(math.floor(2*Y) > height-1):
                        overY = overY + 1
                        newPolygon.append(height-1)
                        Yarr.append(2*Y)
                    else:
                        newPolygon.append(math.floor(2*Y))
                        Yarr.append(2*Y)

                newSegmentation.append(newPolygon)
                newShape['segmentation'] = newSegmentation
                newShape['area'] = shape['properties']['Shape_Area']
                newShape['bbox'] = [ min(Xarr), min(Yarr), (max(Xarr)-min(Xarr)), (max(Yarr)-min(Yarr)) ]
                newShape['iscrowd'] = 0
                newShapeList.append(newShape)
                prevNum = prevNum + 1
        print()
        print("over Y: " + str(overY))
        print("over X: " + str(overX))
        print("neg zeroes: " + str(negZeroCounter))
    return newShapeList
    # jsonDict = {}
    # jsonDict['annotations'] = newShapeList
    # print(len(newShapeList))
    #
    # with open(dstJSON, 'w') as file:
    #     file.write(json.dumps(jsonDict))
#Test
#geoJSONtoCOCO('/data/COA Aerial Data/2017/Austin JPEG2000/Austin_East-NEA2.jp2', '../data/interim/test/Austin_East-NEA2.geojson', '../data/interim/test/json/new.json')
