import os
import pandas as pd

from data_handler import load_data, check_and_convert_types, join_simbad
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb, degrees_to_radians, star_data_calculator
from plotter import plot_3d_scatter, plot_3d_scatter_plotly

def all_stars():

    # get data from ysb, simbad and iau
    df = join_simbad()
        
    # calculate star data such as xyz coords 
    df = star_data_calculator(df)
    
    title='all_stars'

    # plots 3d scatter diagram 
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values,
                                    df.y_coordinate.values,
                                    df.z_coordinate.values,
                                    df.rgb_color.values,
                                    df.star_size.values,
                                    title=title,
                                    lines=False)
            # plot the 3D scatter plot 
    fig1 = plot_3d_scatter_plotly(
        df,                     \
        title=title,            \
        lines=False)



    return title, fig, ax, view 
