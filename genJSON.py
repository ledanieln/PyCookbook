# -*- coding: utf-8 -*-
import glob
import os
import json
from osgeo import gdal
from collections import OrderedDict
from progress.bar import ShadyBar
import vectorProcessing as vp
import itertools

geoJSONList = sorted(glob.glob('/data/coa-interim/geoJSON/train/*.geojson'))
jpgList = sorted(glob.glob('/data/coa-processed/train/coa-training-images/*.jpg'))
dstJSON = '/data/coa-processed/train/annotations.json'

# geoJSONList = sorted(glob.glob('../sample/geojson/2015/*.geojson'))
# jpgList = sorted(glob.glob('../sample/images/2015/*.jpg'))
# dstJSON = '../sample/2015-instances.json'

print(geoJSONList[0])
print(jpgList[0])

##Generate JSON files below
COCOfile = {}
images = []
annotations = []
categories = []

#Load categories
with open('../references/categories-all.json') as jsonFile:
    data = json.load(jsonFile)
    categories = data

bar = ShadyBar('Creating images...', max = len(jpgList))
#Load images
for i in range(len(jpgList)):
    fileName = os.path.basename(jpgList[i]).split('.')[0]
    newImage = {}
    newImage['id'] = i
    src_ds = gdal.Open(jpgList[i], gdal.GA_ReadOnly)
    newImage['width'] = src_ds.RasterXSize
    newImage['height'] = src_ds.RasterYSize
    newImage['file_name'] = fileName + '.jpg'
    images.append(newImage)
    bar.next()
bar.finish()

bar = ShadyBar('Creating annotations...', max = len(geoJSONList))
#Load annotations
prevNum = 0
for i in range(len(geoJSONList)):
    annotations.append(vp.geoJSONtoCOCO(jpgList[i], geoJSONList[i], i, prevNum))
    prevNum = len(annotations)
    bar.next()

annotations = list(itertools.chain.from_iterable(annotations))
bar.finish()

COCOfile['images'] = images
COCOfile['annotations'] = annotations
COCOfile['categories'] = categories

with open(dstJSON, 'w') as file:
     file.write(json.dumps(COCOfile))
