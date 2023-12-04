import os
import sys
import time
import pandas as pd

from data_handler import get_data_frame, get_dictionary, join_simbad
from calculations import star_data_calculator, find_closest_star_view
from plotter import plot_3d_scatter, capture_gif, plot_3d_scatter_plotly
from helper import greek_letter

from matplotlib import pyplot as plt

def constellations(plot=False, gif=False):
    print("Starting Constellation processing...")

    start_time = time.time()

    # load data from the yale bright star catalogue using j2000 coordinates
    df = join_simbad()

    # constellation dictionary is a function that gets the alt_name and combines it with the commmon name
    # alt_name = UMi, common_name = Ursa Major
    constellation_names = get_dictionary('constellation_names')
   
    len_of_df = len(constellation_names)
    counter = 0

    # get both name types from the dictionary
    for common_name, alt_name in constellation_names.items():

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

        elevation, azimuth = find_closest_star_view(df_filtered)

        # plot the 3D scatter plot 
        fig, ax, view, = plot_3d_scatter( 
                df_filtered.x_coordinate.values, \
                df_filtered.y_coordinate.values, \
                df_filtered.z_coordinate.values, \
                df_filtered.rgb_color.values,    \
                df_filtered.star_size.values,    \
                df_filtered.iau_name.values,     \
                title=title,                     \
                view=(elevation, azimuth),       \
                lines=False) 

        # plot the 3D scatter plot 
        fig = plot_3d_scatter_plotly(
                df_filtered,                     \
                title=title,                     \
                view=(elevation, azimuth),       \
                lines=False) 

        # show plot if true
        if plot:
            plt.show()
            plt.close(fig)

        # create gif if true 
        # WILL TAKE ABOUT 33 MINS FOR ALL CONSTELLATIONS
        if gif:
            capture_gif(title, fig, ax, view, of_type='constellation')
            plt.close()

        plt.close()
        counter += 1

        # Calculate the percentage and the elapsed time
        percent_complete = (counter / len_of_df) * 100
        elapsed_time = time.time() - start_time

        # Estimate remaining time
        # Avoid division by zero and handle the case when counter is still 0
        if counter > 0:
            remaining_time = (elapsed_time / counter) * (len_of_df - counter)
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            print(f'\rConstellation Progress: {percent_complete:.2f}% complete - Time remaining: {remaining_minutes}m {remaining_seconds}s', end='', flush=True)
        else:
            print(f'\rConstellation Progress: {percent_complete:.2f}% complete - Time remaining: estimating...', end='', flush=True)

    # After the loop, print the total time taken
    total_time = time.time() - start_time
    total_minutes = int(total_time // 60)
    total_seconds = int(total_time % 60)
    print(f"\nAll constellations processed! Total time: {total_minutes}m {total_seconds}s")

    return None
