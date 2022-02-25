import rasterio
import pandas as pd
import plotly.graph_objects as go

# Crop part of a TIF image --> this info should come from x,y coordinates of prop of interest
#x_center = 104994.91
#y_center = 192612.04

# Clipping a raster file

xmin = 152031.88 - 140
xmax = 152031.88 + 140
ymin = 172013.43 - 140
ymax = 172013.43 + 140


def window_from_extent(xmin, xmax, ymin, ymax, aff):
    col_start, row_start = ~aff * (xmin, ymax)
    col_stop, row_stop = ~aff * (xmax, ymin)
    return ((int(row_start), int(row_stop)), (int(col_start), int(col_stop)))


with rasterio.open(
        'data/DSM/DHMVIIDSMRAS1m_k31.zip/GeoTIFF/DHMVIIDSMRAS1m_k31.tif'
) as src:
    aff = src.transform
    window = window_from_extent(xmin, xmax, ymin, ymax, aff)

    # Read croped array
    arr = src.read(1, window=window)

# Faster way of generating 3D model. Don't need to save as a new TIF file.
df = pd.DataFrame(arr)

# Plot in 3D <-- see Method 2 in Playing with cropped image.py file.
fig = go.Figure(data=[go.Surface(z=df.values)])
fig.show()
