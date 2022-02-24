import rasterio
from rasterio.merge import merge
from rasterio.plot import show

src_dsm = rasterio.open(
    'data/DSM/DHMVIIDSMRAS1m_k31.zip/GeoTIFF/DHMVIIDSMRAS1m_k31.tif')

src_dtm = rasterio.open(
    'data/DTM/DHMVIIDTMRAS1m_k31.zip/GeoTIFF/DHMVIIDTMRAS1m_k31.tif')

src_files_to_mosaic = [src_dsm, src_dtm]

mosaic, out_transform = merge(src_files_to_mosaic)

out_meta = src.meta.copy()

out_meta.update({
    'driver': 'GTiff',
    'height': mosaic.shape[1],
    'width': mosaic.shape[2],
    'transform': out_transform,
})

#print(src_dsm.shape)
#print(src_dtm.shape)
#print(mosaic.shape)

#show(mosaic, cmap='terrain')
