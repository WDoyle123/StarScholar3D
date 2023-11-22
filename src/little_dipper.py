import os
import pandas as pd

from data_handler import load_data, check_and_convert_types
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb, degrees_to_radians
from plotter import plot_3d_scatter

def little_dipper():
    # current directory
    current_dir = os.path.dirname('src') 

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', 'data_j2000.csv')

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    # check if types are correct and convert if otherwise
    df = check_and_convert_types(df)

    # Little Dipper stars in Ursa Minor, alternative names and common names respectivly
    little_dipper_stars = ['1Alp UMi', '23Del UMi', '22Eps UMi', '16Zet UMi', '7Bet UMi', '13Gam UMi', '21Eta UMi']
    ordered_star_names = ['Polaris', 'Yidun', 'Eps UMi', 'Zet UMi', 'Kochab', 'Pherkad', 'Eta UMi']

    df = df[df['alt_name'].isin(little_dipper_stars)]

    # map alternative names to common names
    name_mapping = dict(zip(little_dipper_stars, ordered_star_names))
    
    df['common_name'] = df['alt_name'].map(name_mapping)

    # create order to the stars, this allows for connecting the stars using a line plot in plotter.py
    df['common_name'] = pd.Categorical(df['common_name'], categories=ordered_star_names, ordered=True)
    df = df.sort_values(by='common_name')

    # remove any NaN and zero values found in parallax column
    df = df[(df['parallax'].notna() & df.parallax != 0)]

    # turns degrees to radians (np.sin and np.cos already do this but this will update the df)
    df['dec'] = df.apply(lambda row: degrees_to_radians(row['dec']), axis=1)
    df['ra'] = df.apply(lambda row: degrees_to_radians(row['ra']), axis=1)

    # Calculate x, y, z coordinates and RGB colors, and add them to the df
    df['distance'] = df.apply(lambda row: calculate_distance(row['parallax']), axis=1)

    # create x y z coordinates in the df using distance, declination and right acension
    df['x_coordinate'] = df.apply(lambda row: calculate_x_coordinate((row['distance']), row['dec'], row['ra']), axis=1)
    df['y_coordinate'] = df.apply(lambda row: calculate_y_coordinate((row['distance']), row['dec'], row['ra']), axis=1)
    df['z_coordinate'] = df.apply(lambda row: calculate_z_coordinate((row['distance']), row['dec']), axis=1)

    # creates a color variable to each star (approximatly) 
    df['rgb_color'] = df['bv_color'].apply(bv_color_to_rgb)

    title = 'little_dipper'
    view = (29, -135)

    # plots the Little Dipper asterism
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, df.common_name.values, title=title, view=view)
     
    return title, fig, ax, view
