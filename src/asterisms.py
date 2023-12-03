import os
import sys
import time
import pandas as pd
from matplotlib import pyplot as plt

from data_handler import get_data_frame, get_dictionary, join_simbad
from calculations import star_data_calculator, find_closest_star_view
from plotter import plot_3d_scatter, capture_gif

def asterisms(plot=False, gif=False):
    print("Starting Asterism processing...")

    start_time = time.time()

    asterisms_dictionary = get_dictionary('asterism_names')

    len_of_df = len(asterisms_dictionary)
    counter = 0

    # get both name types from the dictionary
    for asterism_name, hr_names in asterisms_dictionary.items():

        # convert to lower case and if common_name has a space change to underscore
        unchanged_title = asterism_name
        title = asterism_name.lower().replace(' ', '_')

        df = join_simbad()
        
        # .copy to avoid copy of sclice warning
        df_filtered = df[df['hr'].isin(hr_names)].copy()

        # Create a temporary mapping from hr names to indices based on their order in hr_names
        order_mapping = {hr_name: i for i, hr_name in enumerate(hr_names)}

        # Map each hr name in df_filtered to its corresponding index
        df_filtered['order'] = df_filtered['hr'].map(order_mapping)

        # Sort df_filtered by this order
        df_filtered = df_filtered.sort_values('order')

        # Drop the temporary 'order' column
        df_filtered = df_filtered.drop('order', axis=1)

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
                view=(int(elevation) + 90, int(azimuth) - 10),\
                lines=True) 

        # show plot if true
        if plot:
            plt.show()
            plt.close(fig)

        # create gif if true 
        # WILL TAKE ABOUT 3 MINS FOR ALL Asterisms
        if gif:
            capture_gif(title, fig, ax, view, of_type='asterism')
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
            print(f'\rAsterism Progress: {percent_complete:.2f}% complete - Time remaining: {remaining_minutes}m {remaining_seconds}s', end='', flush=True)
        else:
            print(f'\rAsterism Progress: {percent_complete:.2f}% complete - Time remaining: estimating...', end='', flush=True)

    # After the loop, print the total time taken
    total_time = time.time() - start_time
    total_minutes = int(total_time // 60)
    total_seconds = int(total_time % 60)
    print(f"\nAll Asterisms processed! Total time: {total_minutes}m {total_seconds}s")

    return None
