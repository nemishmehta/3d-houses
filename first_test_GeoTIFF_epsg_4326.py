import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from affine import Affine
from pyproj import Proj, transform
import gdal

img = rasterio.open(
    '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DHMVIIDSMRAS1m_k01.zip/GeoTIFF/DHMVIIDSMRAS1m_k01_epsg_4326.tif'
)

full_img = img.read()

print('The shape of the image = ', full_img.shape)

print('Coordinate reference system = ', img.crs)

#show(img)
"""
band_arr = img.read(img.count)
print(band_arr.shape)

px_vals = []

for x in range(6040, 6047):
    for y in range(16900, 17000):
        px_vals.append({'x': x, 'y': y, 'value': band_arr[x, y]})

print(px_vals)
"""
"""
# Get coordinates and corresponding pixel values
T0 = img.transform  # upper-left pixel corner affine transform
p1 = Proj(img.crs)
A = img.read()  # pixel values

# All rows and cols
cols, rows = np.meshgrid(np.arange(A.shape[2]), np.arange(A.shape[1]))

# Get affine transform for pixel centre
T1 = T0 * Affine.translation(0.5, 0.5)

rc2en = lambda r, c: (c, r) * T1

easting, northing = np.vectorize(rc2en, otypes=[float, float])(rows, cols)

p2 = Proj(proj='latlong', datum='WGS84')
longs, lats = transform(p1, p2, easting, northing)
"""
x = 5000
y = 13000
# open the dataset and get the geo transform matrix
ds = gdal.Open(
    '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DHMVIIDSMRAS1m_k01.zip/GeoTIFF/DHMVIIDSMRAS1m_k01_epsg_4326.tif'
)
xoffset, px_w, rot1, yoffset, px_h, rot2 = ds.GetGeoTransform()

# supposing x and y are your pixel coordinate this
# is how to get the coordinate in space.
posX = px_w * x + rot1 * y + xoffset
posY = rot2 * x + px_h * y + yoffset

# shift to the center of the pixel
posX += px_w / 2.0
posY += px_h / 2.0

print(posX, posY)
