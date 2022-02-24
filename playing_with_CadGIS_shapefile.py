import geopandas as gpd
from shapely.geometry import Point
import fiona
import pandas as pd
import plotly.graph_objects as go
import rasterio
import rasterio.mask
"""
fc = fiona.open('data/CadGIS_fiscaal/Shapefile/BpnCapa.shp')
for item in fc:
    first_feature = next(iter(fc))
    #print(first_feature)
"""
"""
print(type(first_feature))

print(first_feature['geometry']['coordinates'])

print(type(first_feature['geometry']['coordinates']))

test = pd.DataFrame(first_feature['geometry']['coordinates'])
print(test)
"""
"""
fig = go.Figure(data=[go.Surface(z=test.values)])
fig.show()
"""
#for item in fiona.open('data/CadGIS_fiscaal/Shapefile/BpnCapa.shp')
# Used the xy coordinates and add 10 to each coordinate
df = gpd.read_file('data/Belgium/Bpn_CaPa_VLA.shp',
                   bbox=(152031.88, 172013.43, 152031.88, 172013.43))
#df = df.set_geometry('geometry')

if df.size == 0:
    df = gpd.read_file('data/Belgium/Bpn_CaPa_BRU.shp',
                       bbox=(152031.88, 172013.43, 152031.88, 172013.43))
elif df.size == 0:
    df = gpd.read_file('data/Belgium/Bpn_CaBu.shp',
                   bbox=(63009.72, 222802.63, 63009.72, 222802.63))

"""
print(df)
print(df.geometry.bounds)

x_min_prop = df.geometry.bounds.iloc[0]['minx']
y_min_prop = df.geometry.bounds.iloc[0]['miny']
x_max_prop = df.geometry.bounds.iloc[0]['maxx']
y_max_prop = df.geometry.bounds.iloc[0]['maxy']

print('xmin = ', x_min_prop)
print('xmax = ', x_max_prop)
print('ymin = ', y_min_prop)
print('ymax = ', y_max_prop)

print(df.Shape_area)

plot_surface = df.iloc[0]['Shape_area']

print(f'Surface of the plot = {plot_surface} m2')

#print(df.index is True)
"""
# Plot polygon of interest in 2D
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(15, 15))

df.loc[[0], 'geometry'].plot(ax=ax)
plt.show()
"""
"""
# Clip raster based on polygon
import json

data = rasterio.open(
    'data/DHMVIIDSMRAS1m_k04.zip/GeoTIFF/DHMVIIDSMRAS1m_k04.tif')


def getFeatures(df):
    # Function to parse features in a manner that rasterio wants them
    return [json.loads(df.to_json())['features'][0]['geometry']]


coords = getFeatures(df)

print(coords)

out_img, out_transform = rasterio.mask.mask(data, shapes=coords, crop=True)

out_meta = data.meta.copy()

out_meta.update({
    'driver': 'GTiff',
    'height': out_img.shape[1],
    'width': out_img.shape[2],
    'transform': out_transform
})

with rasterio.open('Test.tif', 'w', **out_meta) as dest:
    dest.write(out_img)

src = rasterio.open('Test.tif')

arr = src.read(1)

#print(type(out_img))
#print(out_img.shape)

df_cropped = pd.DataFrame(arr)

fig = go.Figure(data=[go.Surface(z=df_cropped.values)])
fig.show()
"""
"""
# Plot polygon of interest in 2D
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(15, 15))

df.loc[[0], 'geometry'].plot(ax=ax)
plt.show()
"""
#print(df['geometry'][0])
"""

point = Point(139001.002700001, 200517.74399999902)

for i in range(10):
    if point.within(df['geometry'][i]) is True:
        print(df['geometry'][i])
"""
#print(df['geometry'].within(point))

#if point.within(df['geometry'][0]) is True:
#    print('Success')

#print(point.within(df['geometry'][0]))

#for i in test:
#if 139036.86869999766 in test:
#    print(i)
"""
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(15, 15))

df.loc[[9], 'geometry'].plot(ax=ax)
plt.show()
"""