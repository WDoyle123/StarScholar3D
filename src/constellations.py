import os
import pandas as pd

from data_handler import load_data, check_and_convert_types
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb, degrees_to_radians, star_data_calculator
from plotter import plot_3d_scatter

def ursa_major():

    # current directory
    current_dir = os.path.dirname('src')

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', 'data_j2000.csv')

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    # check if types are correct and convert if otherwise
    df = check_and_convert_types(df)

    # gets stars in the ursa major constellation
    df = df[df['alt_name'].str.contains('UMa')]
    print(df)
    print(len(df))
    
    # apply calculations such as getting coordinates and color 
    df = star_data_calculator(df)

    title = 'ursa_major'

    # plots ursa major constellation
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, title=title)

    return title, fig, ax, view
