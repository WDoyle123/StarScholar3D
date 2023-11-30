import os
import pandas as pd

from data_handler import get_data_frame, constellation_dictionary
from calculations import star_data_calculator
from plotter import plot_3d_scatter, capture_gif
from helper import greek_letter

from matplotlib import pyplot as plt

def constellations(plot=False, gif=False):

    # load data from the yale bright star catalogue using j2000 coordinates
    df = get_data_frame('data_j2000.csv')

    # constellation dictionary is a function that gets the alt_name and combines it with the commmon name
    # alt_name = UMi, common_name = Ursa Major
    constellation_names = constellation_dictionary(df)
   
    # get both name types from the dictionary
    for alt_name, common_name in constellation_names.items():

        # convert to lower case and if common_name has a space change to underscore
        unchanged_title = common_name
        title = common_name.lower().replace(' ', '_')

        # creates a boolean mask if the data frame contains an alt_name. 
        # False also for NaN
        mask = df['alt_name'].str.contains(alt_name, na=False)

        # apply boolean mask to the dataframe
        df_filtered = df[mask]

        # Del and Tau are both Greek letters and short for Delphinus and Taurus repectivley 
        # But stars are designated by greek letters such as Alp UMi - Polaris
        # This function filters the df so that stars such as Tau UMi do not appear in Taurus constellation
        if alt_name == 'Del' or alt_name == 'Tau':
            df_filtered = greek_letter(df_filtered, alt_name)

        # Calculate the coordinates and colour from right acension and declination aswell as bv colour 
        df_filtered = star_data_calculator(df_filtered)

        # plot the 3D scatter plot 
        fig, ax, view, = plot_3d_scatter( 
                df_filtered.x_coordinate.values, \
                df_filtered.y_coordinate.values, \
                df_filtered.z_coordinate.values, \
                df_filtered.rgb_color.values, \
                title=title, \
                lines=False) 

        # show plot if true
        if plot:
            plt.show()
            plt.close(fig)

        # create gif if true 
        # WILL TAKE ABOUT 33 MINS FOR ALL CONSTELLATIONS
        if gif:
            print(f'Creating gif for: {unchanged_title}')
            capture_gif(title, fig, ax, view, of_type='constellation')
            plt.close()

    # plt close needed due to the generation of many graphs in the function
    plt.close()
    return None
