import os
import pandas as pd

from data_handler import load_data, check_and_convert_types, get_data_frame
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb, degrees_to_radians, star_data_calculator
from plotter import plot_3d_scatter

def ursa_major():
    
    # naming figure and gif
    title = 'ursa_major'

    # get data from catalogue using j2000 coordinates
    df = get_data_frame('data_j2000.csv')

    # gets stars in the ursa major constellation
    df = df[df['alt_name'].str.contains('UMa')]
    
    # apply calculations such as getting coordinates and color 
    df = star_data_calculator(df)

    # plots ursa major constellation
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, title=title, lines=False)

    return title, fig, ax, view

def ursa_minor():

    # naming figure and gif
    title = 'ursa_minor'
    
    # get data from catalogue using j2000 coordinates
    df = get_data_frame('data_j2000.csv')

    # gets stars in the ursa minor constellation
    df = df[df['alt_name'].str.contains('UMi')]
    
    # apply calculations such as getting coordinates and color 
    df = star_data_calculator(df)

    # plots ursa major constellation
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, title=title, lines=False)

    return title, fig, ax, view
