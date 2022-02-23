import geopandas as gpd
from shapely.geometry import Point
import fiona
import pandas as pd
import plotly.graph_objects as go
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
df = gpd.read_file('data/CadGIS_fiscaal/Shapefile/BpnCapa.shp',
                   bbox=(63009.72, 222802.63, 63019.72, 222812.63))
#df = df.set_geometry('geometry')

print(df)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(15, 15))

df.loc[[0], 'geometry'].plot(ax=ax)
plt.show()

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