#import rasterProcessing as rp
import vectorProcessing as vp
import glob
import os
import json
from collections import OrderedDict
from osgeo import gdal
from progress.bar import IncrementalBar

#2017
year = '2013-'
fileList = sorted(glob.glob('/data/COA Aerial Data/2013/JP2/*.jp2'))

bar = IncrementalBar('JPEG200 to JPEG...', max = len(fileList))

for file in fileList:
    #Get the file name for the JP2
    fileName = os.path.basename(file).split('.')[0]
    #Input where you want the new JPG to be
    jpgPath = '/data/coa-processed/train/coa-training-images/' + year + fileName + '.jpg'
    #Convert and place into the jpgPath
    #rp.convertJP2toJPG(file, jpgPath)
    #Generate the corresponding clipped geoJSON using the jpg
    vp.clipPolygonByRaster(jpgPath, '/data/coa-interim/geoJSON/train/', '../data/raw/TX_STATE_DATA.gdb', 'planimetrics_2013')
    bar.next()

bar.finish()
