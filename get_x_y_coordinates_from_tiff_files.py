import rasterio

xy_bounds_dict = dict()


def get_xy_bounds():
    """
    This function iterates over all the TIF files and creates a dictionary of the xy bounds of each file.
    """
    for i in range(1, 10):
        with rasterio.open(
                f'data/DHMVIIDSMRAS1m_k0{i}.zip/GeoTIFF/DHMVIIDSMRAS1m_k0{i}.tif'
        ) as src:
            up_left = src.transform * (0, 0)
            bot_right = src.transform * (src.width, src.height)
            xy_bounds_dict[f'DHMVIIDSMRAS1m_k0{i}.tif'] = [
                up_left[0], bot_right[0], bot_right[1], up_left[1]
            ]

    for i in range(10, 44):
        with rasterio.open(
                f'data/DHMVIIDSMRAS1m_k{i}.zip/GeoTIFF/DHMVIIDSMRAS1m_k{i}.tif'
        ) as src:
            # This code will be used to iterate over all DSM files
            up_left = src.transform * (0, 0)
            bot_right = src.transform * (src.width, src.height)
            xy_bounds_dict[f'DHMVIIDSMRAS1m_k{i}.tif'] = [
                up_left[0], bot_right[0], bot_right[1], up_left[1]
            ]


def get_final_tif():
    """
    This function iterates over xy_bounds dict to find TIF file which contains xy coordinates of interest.
    """
    for key, value in xy_bounds_dict.items():
        if ((x > value[0] and x < value[1])
                and (y > value[2] and y < value[3])):
            return key


get_xy_bounds()
# Jain Temple
#x = 151934.29
#y = 207178.86

# Blankenberge
#x = 63009.72
#y = 222802.63

# St-Pietersabdij
x = 104994.91
y = 192612.04

tif_file = get_final_tif()

print(tif_file)
