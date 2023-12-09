import os
import sys
import time
import pandas as pd
from matplotlib import pyplot as plt

from data_handler import get_data_frame, get_dictionary, join_simbad
from calculations import star_data_calculator, find_closest_star_view
from plotter import plot_3d_scatter, capture_gif, plot_3d_scatter_plotly

from multiprocessing import Pool

def asterisms(plot=False, gif=False):
    """
    Function to process asterisms in parallel using multiprocessing.

    Args:
    plot (bool): If True, displays the generated plot for each asterism.
    gif (bool): If True, generates a gif for each asterism.

    This function fetches the dictionary of asterisms, sets up multiprocessing, and processes each
    asterism using multiple processes for improved performance.
    """
    print("Starting Asterism processing with Multiprocessing...")
    start_time = time.time()

    # Fetching the asterism data
    asterisms_dictionary = get_dictionary('asterism_names')
    asterism_items = list(asterisms_dictionary.items())

    # Determine the number of processes to use, leaving one core free
    num_processes = os.cpu_count() - 1

    with Pool(processes=num_processes) as pool:
        # Parallel processing of each asterism
        args = [(item, plot, gif) for item in asterism_items]
        pool.starmap(process_asterism, args)

    total_time = time.time() - start_time
    print(f"All Asterisms processed in {total_time:.2f} seconds")

def process_asterism(asterism_data, plot=False, gif=False):
    """
    Worker function to process a single asterism.

    Args:
    asterism_data (tuple): A tuple containing the name of the asterism and a list of HR names associated with it.
    plot (bool): If True, displays the generated plot.
    gif (bool): If True, generates a gif of the plot.

    This function takes the data for a single asterism, processes it, and optionally generates a plot or gif.
    """
    # get both name types from the dictionary
    asterism_name, hr_names = asterism_data

    print(f'Processing Asterism: {asterism_name}')

    # convert to lower case and if common_name has a space change to underscore
    unchanged_title = asterism_name
    title = asterism_name.lower().replace(' ', '_')

    # get data from ysb and simbad 
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

    # plot the 3D scatter plot 
    fig1 = plot_3d_scatter_plotly(
            df_filtered,                    \
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
    return None
