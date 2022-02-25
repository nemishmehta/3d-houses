import rasterio
import pandas as pd
import plotly.graph_objects as go

xmin = 152031.88 - 140
xmax = 152031.88 + 140
ymin = 172013.43 - 140
ymax = 172013.43 + 140


def window_from_extent(src, xmin, xmax, ymin, ymax, aff):

    # Method 1 --> use index of xy coordinates to get exact pixels
    row_start, col_start = src.index(xmin, ymax)
    row_stop, col_stop = src.index(xmax, ymin)

    # Method 2 --> use inverse of affine to get exact pixels
    """
    col_start, row_start = ~aff * (xmin, ymax)
    col_stop, row_stop = ~aff * (xmax, ymin)
    """
    return ((int(row_start), int(row_stop)), (int(col_start), int(col_stop)))


with rasterio.open(
        'data/DSM/DHMVIIDSMRAS1m_k31.zip/GeoTIFF/DHMVIIDSMRAS1m_k31.tif'
) as src_dsm:
    aff = src_dsm.transform
    #meta = src.meta.copy() --> not required
    window_dsm = window_from_extent(src_dsm, xmin, xmax, ymin, ymax, aff)

    # Read croped array
    arr_dsm = src_dsm.read(1, window=window_dsm)

with rasterio.open(
        'data/DTM/DHMVIIDTMRAS1m_k31.zip/GeoTIFF/DHMVIIDTMRAS1m_k31.tif'
) as src_dtm:
    aff = src_dtm.transform
    window_dtm = window_from_extent(src_dtm, xmin, xmax, ymin, ymax, aff)

    # Read croped array
    arr_dtm = src_dtm.read(1, window=window_dtm)

chm_arr = arr_dsm - arr_dtm

df = pd.DataFrame(chm_arr)
#print(df)

# Plot in 3D <-- see Method 2 in Playing with cropped image.py file.
fig = go.Figure(data=[go.Surface(z=df.values)])
fig.show()