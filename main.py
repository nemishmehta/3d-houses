from utils.plot_3D_house import get_prop_coord, get_xy_bounds_tif_files, get_final_tif, get_plot_area_shape, get_cropped_area, get_3D_model

if __name__ == '__main__':
    address, x_coord, y_coord = get_prop_coord()

    #xy_bounds_dict = dict()
    xy_bounds_dict = get_xy_bounds_tif_files()

    tif_file = get_final_tif(xy_bounds_dict, x_coord, y_coord)
    print('The TIF file for this property is: ', tif_file)

    plot_surface, x_min_prop, y_min_prop, x_max_prop, y_max_prop = get_plot_area_shape(
        x_coord, y_coord)

    dsm_arr = get_cropped_area('DSM', tif_file, x_min_prop, x_max_prop,
                               y_min_prop, y_max_prop)

    dtm_arr = get_cropped_area('DTM', tif_file, x_min_prop, x_max_prop,
                               y_min_prop, y_max_prop)

    get_3D_model(dsm_arr, dtm_arr, address, plot_surface)
