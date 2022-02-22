import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from affine import Affine
from pyproj import Proj, transform
import plotly.graph_objects as go

# Crop part of a TIF image --> this info should come from x,y coordinates of prop of interest
x_center = 104994.91
y_center = 192612.04

xmin = x_center - 40
xmax = x_center + 40
ymin = y_center - 40
ymax = y_center + 40


def window_from_extent(xmin, xmax, ymin, ymax, aff):
    col_start, row_start = ~aff * (xmin, ymax)
    col_stop, row_stop = ~aff * (xmax, ymin)
    return ((int(row_start), int(row_stop)), (int(col_start), int(col_stop)))


with rasterio.open(
        '/home/nemish/BeCode/BeCode_Projects/3d-houses/data/DHMVIIDSMRAS1m_k22.zip/GeoTIFF/DHMVIIDSMRAS1m_k22.tif'
) as src:
    aff = src.transform
    meta = src.meta.copy()
    window = window_from_extent(xmin, xmax, ymin, ymax, aff)

    # Read croped array
    arr = src.read(1, window=window)

    # Update dataset metadata (if you need it)
    meta.update(height=window[0][1] - window[0][0],
                width=window[1][1] - window[1][0],
                transform=src.window_transform(window))

    # Remove transform key-value pair because the affine key already exists <-- not required
    #meta.pop('transform', None)

# Save arr in a new tif file
"""
with rasterio.open('Test.tif', 'w', **meta) as dst:
    dst.write(arr, 1)
"""
# Faster way of generating 3D model. Don't need to save as a new TIF file.
df = pd.DataFrame(arr)

# Plot in 3D <-- see Method 2 in Playing with cropped image.py file.
fig = go.Figure(data=[go.Surface(z=df.values)])
fig.show()