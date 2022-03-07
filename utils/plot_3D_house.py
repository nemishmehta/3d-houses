import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import rasterio
import rasterio.mask
import requests


def get_prop_coord():
    """
    Use user input address to find xy coordinates of property
    """
    address = input('Enter your address: ')
    response = requests.get(f'https://loc.geopunt.be/v4/Location?q={address}')

    address_dict = response.json()

    x_coord = address_dict['LocationResult'][0]['BoundingBox']['LowerLeft'][
        'X_Lambert72']
    y_coord = address_dict['LocationResult'][0]['BoundingBox']['LowerLeft'][
        'Y_Lambert72']

    return address, x_coord, y_coord


def get_xy_bounds_tif_files():
    """
    This function iterates over all the TIF files and creates a dictionary of the xy bounds of each file.
    """
    xy_bounds_dict = dict()

    for i in range(1, 10):
        with rasterio.open(
                f'data/DSM/DHMVIIDSMRAS1m_k0{i}.zip/GeoTIFF/DHMVIIDSMRAS1m_k0{i}.tif'
        ) as src:
            up_left = src.transform * (0, 0)
            bot_right = src.transform * (src.width, src.height)
            xy_bounds_dict[f'0{i}'] = [
                up_left[0], bot_right[0], bot_right[1], up_left[1]
            ]

    for i in range(10, 44):
        with rasterio.open(
                f'data/DSM/DHMVIIDSMRAS1m_k{i}.zip/GeoTIFF/DHMVIIDSMRAS1m_k{i}.tif'
        ) as src:
            # This code will be used to iterate over all DSM files
            up_left = src.transform * (0, 0)
            bot_right = src.transform * (src.width, src.height)
            xy_bounds_dict[f'{i}'] = [
                up_left[0], bot_right[0], bot_right[1], up_left[1]
            ]

    return xy_bounds_dict


def get_final_tif(xy_bounds_dict, x, y):
    """
    This function iterates over xy_bounds dict to find TIF file which contains xy coordinates of interest.
    """
    for key, value in xy_bounds_dict.items():
        if ((x > value[0] and x < value[1])
                and (y > value[2] and y < value[3])):
            return key


def get_plot_area_shape(x, y):
    """
    This function uses x,y coordinate to get a polygon of the total plot area.
    """
    df = gpd.read_file('data/Belgium/Bpn_CaPa_VLA.shp', bbox=(x, y, x, y))

    if df.size == 0:
        df = gpd.read_file('data/Belgium/Bpn_CaPa_BRU.shp', bbox=(x, y, x, y))
    elif df.size == 0:
        df = gpd.read_file('data/Belgium/Bpn_CaBu.shp', bbox=(x, y, x, y))

    plot_surface = round(df.iloc[0]['Shape_area'], 2)

    x_min = df.geometry.bounds.iloc[0]['minx']
    y_min = df.geometry.bounds.iloc[0]['miny']
    x_max = df.geometry.bounds.iloc[0]['maxx']
    y_max = df.geometry.bounds.iloc[0]['maxy']

    # Return surface of the plot area and the xy bounds of property
    return plot_surface, x_min, y_min, x_max, y_max


def get_cropped_area(file_type, tif_file, x_min_prop, x_max_prop, y_min_prop,
                     y_max_prop):
    with rasterio.open(
            f'data/{file_type}/DHMVII{file_type}RAS1m_k{tif_file}.zip/GeoTIFF/DHMVII{file_type}RAS1m_k{tif_file}.tif'
    ) as src:

        row_start, col_start = src.index(x_min_prop, y_max_prop)
        row_stop, col_stop = src.index(x_max_prop, y_min_prop)

        window = ((int(row_start), int(row_stop)), (int(col_start),
                                                    int(col_stop)))

        # Read croped array
        arr = src.read(1, window=window)

        return arr


def get_3D_model(dsm_arr, dtm_arr, address, plot_surface):
    """
    Use DSM & DTM arrays to plot a 3D model 
    """
    chm_arr = dsm_arr - dtm_arr
    df_cropped = pd.DataFrame(chm_arr)

    fig = go.Figure(data=[go.Surface(z=df_cropped.values)])
    fig.update_layout(
        title=f'Address: {address},   Plot surface: {plot_surface} m2')
    fig.show()