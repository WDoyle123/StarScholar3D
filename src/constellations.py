import os
import sys
import time
import pandas as pd
from matplotlib import pyplot as plt

from data_handler import get_data_frame, get_dictionary, join_simbad
from calculations import star_data_calculator, find_closest_star_view
from plotter import plot_3d_scatter, capture_gif, plot_3d_scatter_plotly
from helper import greek_letter

from multiprocessing import Pool

def constellations(plot=False, gif=False):
    """
    Function to process constellations in parallel using multiprocessing.

    Args:
    plot (bool): If True, displays the generated plot for each constellation.
    gif (bool): If True, generates a gif for each constellation.

    This function fetches the dictionary of constellations, sets up multiprocessing, and processes each
    constellation using multiple processes for improved performance.
    """
    print("Starting Constellation processing with Multiprocessing...")
    start_time = time.time()

    # Fetching the constellation data
    constellation_dictionary = get_dictionary('constellation_names')
    constellation_items = list(constellation_dictionary.items())

    # Determine the number of processes to use, leaving some cores free
    num_processes = round(os.cpu_count() / 2)

    with Pool(processes=num_processes) as pool:
        # Parallel processing of each constellation
        args = [(item, plot, gif) for item in constellation_items]
        pool.starmap(process_constellation, args)

    total_time = time.time() - start_time
    print(f"All Constellations processed in {total_time:.2f} seconds")

def process_constellation(constellation_data, plot=False, gif=False):
    """
    Worker function to process a single constellation.

    Args:
    constellation_data (tuple): A tuple containing the name of the constellation and its alt_name
    plot (bool): If True, displays the generated plot.
    gif (bool): If True, generates a gif of the plot.

    This function takes the data for a single constellation, processes it, and optionally generates a plot or
    gif.
    """
    # get common name (Ursa Major) and alt_name (UMa)
    common_name, alt_name = constellation_data

    print(f'Processing Constellation: {common_name}')

    # get data from YSB, IAU and SIMBAD
    df = join_simbad()

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
    fig1 = plot_3d_scatter_plotly(
            df_filtered,                     \
            title=title,                     \
            view=(elevation, azimuth),       \
            lines=False) 

    # show plot if true
    if plot:
        plt.show()
        plt.close(fig)

    # create gif if true 
    # WILL TAKE ABOUT 10 MINS 6 CORES FOR ALL CONSTELLATIONS
    if gif:
        capture_gif(title, fig, ax, view, of_type='constellation')
        plt.close()

    plt.close()
    return None
