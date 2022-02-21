import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from affine import Affine
from pyproj import Proj, transform

#img = rasterio.open(
#    '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DHMVIIDSMRAS1m_k36.zip/GeoTIFF/DHMVIIDSMRAS1m_k36.tif'
#)

#Get info on TIF file
#show(img)

# Crop part of a TIF image --> Attempt 1
xmin = 46635.5
xmax = 46803.6
ymin = 153181.6
ymax = 153419.8


def window_from_extent(xmin, xmax, ymin, ymax, aff):
    col_start, row_start = ~aff * (xmin, ymax)
    col_stop, row_stop = ~aff * (xmax, ymin)
    return ((int(row_start), int(row_stop)), (int(col_start), int(col_stop)))


with rasterio.open(
        '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DHMVIIDSMRAS1m_k36.zip/GeoTIFF/DHMVIIDSMRAS1m_k36.tif'
) as src:
    full_img = src.read()
    aff = src.transform
    meta = src.meta.copy()
    window = window_from_extent(xmin, xmax, ymin, ymax, aff)

    # Read croped array
    arr = src.read(1, window=window)

    # Update dataset metadata (if you need it)
    meta.update(height=window[0][1] - window[0][0],
                width=window[1][1] - window[1][0],
                affine=src.window_transform(window))

    meta.pop('transform', None)

print('src shape = ', src.shape)
print(f'src type: {type(src)}')
print('arr shape = ', arr.shape)
print(f'crop type: {type(arr)}')

print('Full image shape = ', full_img.shape)
print('Full image type = ', type(full_img))

# Plot arr
#plt.plot(arr)
#plt.show()

# Figure out how to avoid removing band info while cropping image and using it to build a 3D model.
#show(arr, transform=src.window_transform(window))

# Save arr in a new tif file
with rasterio.open('Test.tif', 'w', **meta) as dst:
    dst.write(arr, 1)
"""
# Crop part of a TIF image --> Attempt 2
xmin = 46635.5
xmax = 46803.6
ymin = 153181.6
ymax = 153419.8

window = rasterio.windows.Window(xmin, xmax, ymin, ymax)

with rasterio.open(
        '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DHMVIIDSMRAS1m_k36.zip/GeoTIFF/DHMVIIDSMRAS1m_k36.tif'
) as src:
    subset = src.read(1, window=window)

plt.figure(figsize=(16, 18.5))
plt.imshow(subset)
"""
"""
full_img = img.read()

print('The shape of the image = ', full_img.shape)

print('Number of bands = ', img.count)

print('Coordinate reference system = ', img.crs)

print(f'Raster description: {img.descriptions}')

print("Geotransform: ", img.transform)

#print(f'Metadata: {img.meta}\n')

#print('Georeferencing: ', img.bounds)

print(img.crs)

print(img.transform)

print(band_arr[0][-1])

print(img.width)

print(img.height)
"""
"""
# Trying to read pixel value in each cell
band_arr = img.read(img.count)
print(band_arr.shape)

px_vals = []

for x in range(8990, 9000):
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

print(longs)
"""