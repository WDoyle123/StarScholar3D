import os
import pandas as pd

from data_handler import load_data, check_and_convert_types
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb, degrees_to_radians
from plotter import plot_3d_scatter

def all_stars():
    # current directory
    current_dir = os.path.dirname('src')

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', 'data_j2000.csv')

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    # check if types are correct and convert if otherwise
    df = check_and_convert_types(df)

    df = star_data_calculator(df)
    
    title='all_stars'

    # plots 3d scatter diagram 
    fig, ax, view = plot_3d_scatter(x_coordinates_array, y_coordinates_array, z_coordinates_array, rgb_colors, title=title)

    return title, fig, ax, view 
