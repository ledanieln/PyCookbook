from osgeo import gdal
from shapely import geometry
import numpy as np

src_path = '../wise_images/2015/test.jpeg'
dst_path = '../wise_images/2015/test_5x.jpeg'

def convertJP2toJPG(src, dst):
    """Converts JPEG2000 into JPEG"""
    src_ds = gdal.Open(src, gdal.GA_ReadOnly)

    # Get Source GeoTransform and Projection
    src_geotransform = src_ds.GetGeoTransform()
    src_projection = src_ds.GetProjection()

    # Create an In-Memory Raster with size according to Source Raster
    fileformat = "MEM"
    driver = gdal.GetDriverByName(fileformat)
    dst_ds = driver.Create('', src_ds.RasterXSize, src_ds.RasterYSize, 3)

    # Get the 3 destination raster bands
    dst_band1 = dst_ds.GetRasterBand(1)
    dst_band2 = dst_ds.GetRasterBand(2)
    dst_band3 = dst_ds.GetRasterBand(3)

    # Read in source raster bands as NumPy arrays
    sb1_array = np.array(src_ds.GetRasterBand(1).ReadAsArray())
    sb2_array = np.array(src_ds.GetRasterBand(2).ReadAsArray())
    sb3_array = np.array(src_ds.GetRasterBand(3).ReadAsArray())

    # Write back the source bands into the in-memory raster
    dst_band1.WriteArray(sb1_array)
    dst_band2.WriteArray(sb2_array)
    dst_band3.WriteArray(sb3_array)

    # Set GeoTransform and Projection to match source raster
    dst_ds.SetGeoTransform(src_geotransform)
    dst_ds.SetProjection(src_projection)

    # Create JPEG Driver
    driver = gdal.GetDriverByName("JPEG")

    # Create a copy of the in-memory raster using JPEG Driver
    driver.CreateCopy(dst, dst_ds, strict=0)

    print("Conversion from JPEG2000 to JPEG Complete!")

def resampleRaster(src, dst, multiplier):
    """Resamples raster according to multiplier"""

    src_ds = gdal.Open(src, gdal.GA_ReadOnly)
    resolution = src_ds.GetGeoTransform()[1]
    src_projection = src_ds.GetProjection()
    newRes = resolution*multiplier

    gdal.Translate(dst, src_ds, outputSRS=src_projection, format='JPEG', xRes=newRes, yRes=newRes)
    dst_ds = gdal.Open(dst, gdal.GA_ReadOnly)
    dstRes = dst_ds.GetGeoTransform()[1]

    print("new size is: " + str(dst_ds.RasterXSize) + " x " + str(dst_ds.RasterYSize))

def generateBoundaryIndex(src):
    """Generates image boundary geometry."""

    gdalSrc = gdal.Open(src, gdal.GA_ReadOnly)
    upx, xres, xskew, upy, yskew, yres = gdalSrc.GetGeoTransform()
    cols = gdalSrc.RasterXSize
    rows = gdalSrc.RasterYSize

    ulx = upx
    uly = upy

    lrx = upx + cols*xres + rows*xskew
    lry = upy + cols*yskew + rows*yres

    boundaryList = [ulx, uly, lrx, lry]
    
    return boundaryList
