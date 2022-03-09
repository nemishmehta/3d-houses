import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import rasterio
import rasterio.mask
import streamlit as st


def get_prop_coord(address_dict):
    """
    Use user input address to find xy coordinates of property
    """
    x_coord = address_dict['LocationResult'][0]['BoundingBox']['LowerLeft'][
        'X_Lambert72']
    y_coord = address_dict['LocationResult'][0]['BoundingBox']['LowerLeft'][
        'Y_Lambert72']

    return x_coord, y_coord


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
    return plot_surface, x_min, y_min, x_max, y_max, df.geometry


def get_cropped_area(file_type, tif_file, x_min_prop, x_max_prop, y_min_prop,
                     y_max_prop, plot_polygon):
    """
    This function is used to get the required cropped area from the specific DSM and DTM files.
    """
    with rasterio.open(
            f'data/{file_type}/DHMVII{file_type}RAS1m_k{tif_file}.zip/GeoTIFF/DHMVII{file_type}RAS1m_k{tif_file}.tif'
    ) as src:
        # Method 1 --> Does not plot attached properties properly
        # row_start, col_start = src.index(x_min_prop, y_max_prop)
        # row_stop, col_stop = src.index(x_max_prop, y_min_prop)

        # window = ((int(row_start), int(row_stop)), (int(col_start),
        #                                             int(col_stop)))

        # # Read croped array
        # arr = src.read(1, window=window)

        # Method 2 --> Does not plot ground features
        arr, _ = rasterio.mask.mask(src,
                                    plot_polygon,
                                    crop=True,
                                    nodata=None,
                                    filled=True,
                                    indexes=1)

        return arr


def get_3D_model(dsm_arr, dtm_arr, address, plot_surface):
    """
    Use DSM & DTM arrays to plot a 3D model 
    """
    chm_arr = dsm_arr - dtm_arr
    df_cropped = pd.DataFrame(chm_arr)

    fig = go.Figure(
        data=[go.Surface(z=df_cropped.values, colorscale='sunsetdark')])
    fig.update_layout(scene=dict(xaxis=dict(showticklabels=False,
                                            visible=False),
                                 yaxis=dict(showticklabels=False,
                                            visible=False),
                                 zaxis=dict(showticklabels=False,
                                            visible=False)),
                      autosize=False,
                      width=800,
                      height=800)
    fig.update_traces(showscale=False)

    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5

    fig.update_layout(
            scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye),
            updatemenus=[dict(type='buttons',
                    showactive=False,
                    y=1,
                    x=0.8,
                    xanchor='left',
                    yanchor='bottom',
                    pad=dict(t=45, r=10),
                    buttons=[dict(label='Play',
                                    method='animate',
                                    args=[None, dict(frame=dict(duration=5, redraw=True), 
                                                                transition=dict(duration=0),
                                                                fromcurrent=True,
                                                                mode='immediate'
                                                                )]
                                                )
                                        ]
                                )
                            ]
    )


    def rotate_z(x, y, z, theta):
        w = x+1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z

    frames=[]
    for t in np.arange(0, 6.26, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
    fig.frames=frames

    st.write('The address is: ', address)
    st.write(f'The plot area is: {str(plot_surface)}m2')

    st.plotly_chart(fig, use_container_width=False)
