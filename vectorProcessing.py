import subprocess
import fiona
import glob
import time
import rasterProcessing as rp
import os
import shapely
import json

# indexStr = glob.glob('../data/interim/2017/*.shp')
# clip_src = indexStr[1]
# print(indexStr)

def clipPolygonByRaster(src_raster, dstPath, gdbPath, gdbTable):
    clip_src = rp.generateBoundaryIndex(src_raster)
    xmin = str(clip_src[0])
    ymin = str(clip_src[1])
    xmax = str(clip_src[2])
    ymax = str(clip_src[3])

    attributesSaved = 'SOURCE, FEATURE, SHAPE_AREA'

    outFileName = dstPath + os.path.basename(src_raster).split('.')[0] + ".geojson"

    print("Beginning Clip")
    start = time.clock()

    print(type(xmin))

    p = subprocess.Popen(["/usr/bin/ogr2ogr", "-f", "GeoJSON", "-select", attributesSaved, "-spat", xmin, ymin, xmax, ymax, "-clipsrc", "spat_extent", outFileName, gdbPath, gdbTable])
    print('Clipped in %.5f seconds' % (time.clock()-start))

#Test:
#clipPolygonByRaster('/data/COA Aerial Data/2017/Austin JPEG2000/Austin_East-NEA2.jp2', '../data/interim/test/', '../data/raw/TX_STATE_DATA.gdb', 'planimetrics_2017')

def geoJSONtoCOCO(src_raster, srcGeoJSON, dstJSON):
    clip_src = rp.generateBoundaryIndex(src_raster)
    xmin = clip_src[0]
    ymin = clip_src[1]
    xmax = clip_src[2]
    ymax = clip_src[3]
    fileName = os.path.basename(src_raster).split('.')[0]

    newShapeList = []
    #IMPORTANT NOTE: This algorithm removes multipolygons. These are shape files with multiple polygons in them. The ID will be different than the original dataset.
    with fiona.open(srcGeoJSON) as shapes:
        i = 0
        for shape in shapes:
            if not shape['geometry']['type'] == 'MultiPolygon':
                newShape = {}
                newShape['id'] = i
                newShape['image_id'] = str(fileName)
                newShape['category_id'] = str(shape['properties']['FEATURE'])
                newShape['area'] = shape['properties']['Shape_Area']
                newShape['iscrowd'] = 0

                newPolygon = []
                Xarr = []
                Yarr = []

                for coordPair in shape['geometry']['coordinates'][0]:
                        newCoordPair = []
                        X = coordPair[0] - xmin
                        Y = -1 * (coordPair[1] - ymax)
                        newCoordPair.append(X)
                        newCoordPair.append(Y)
                        newPolygon.append(tuple(newCoordPair))
                        Xarr.append(X)
                        Yarr.append(Y)

                newShape['bbox'] = [ (min(Xarr), min(Yarr)), (max(Xarr), min(Yarr)), (max(Xarr), max(Yarr)), (min(Xarr), max(Yarr)) ]
                newShape['segmentation'] = newPolygon
                newShapeList.append(newShape)
                i = i + 1

    print(len(newShapeList))

    with open(dstJSON, 'w') as file:
        file.write(json.dumps(newShapeList))
#Test
#geoJSONtoCOCO('/data/COA Aerial Data/2017/Austin JPEG2000/Austin_East-NEA2.jp2', '../data/interim/test/Austin_East-NEA2.geojson', '../data/interim/test/json/new.json')
