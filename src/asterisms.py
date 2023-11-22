import os
import pandas as pd

from data_handler import load_data, check_and_convert_types
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb, degrees_to_radians, star_data_calculator
from plotter import plot_3d_scatter

def big_dipper():

    # current directory
    current_dir = os.path.dirname('src') 

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', 'data_j2000.csv')

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    # check if types are correct and convert if otherwise
    df = check_and_convert_types(df)

    # Big Dipper stars in Ursa Major, alternative names and common names respectivly
    big_dipper_stars = ['79Zet UMa', '77Eps UMa', '69Del UMa', '64Gam UMa', '48Bet UMa', '50Alp UMa', '85Eta UMa']
    ordered_star_names = ['Alkaid', 'Mizar', 'Alcor', 'Alioth', 'Megrez', 'Dubhe', 'Merak', 'Phecda']

    # filter the df to include only the Big Dipper stars
    df = df[df['alt_name'].isin(big_dipper_stars)]

    # map alternative names to common names
    name_mapping = {
        '85Eta UMa': 'Alkaid',    
        '79Zet UMa': 'Mizar',
        '77Eps UMa': 'Alioth',
        '69Del UMa': 'Megrez',
        '64Gam UMa': 'Phecda',
        '48Bet UMa': 'Merak',
        '50Alp UMa': 'Dubhe'
    }
    
    # apply mapping
    df['common_name'] = df['alt_name'].map(name_mapping)

    # manually adjust the entries for Mizar and Alcor since they share name in data_j2000.csv
    mizar_coords = (200.9850, 54.9217)
    alcor_coords = (200.9812, 54.9253)

    for index, row in df.iterrows():
        if row['alt_name'] == '79Zet UMa':
            coords = (row['ra'], row['dec'])
            if coords == mizar_coords:
                df.at[index, 'common_name'] = 'Mizar'
            elif coords == alcor_coords:
                df.at[index, 'common_name'] = 'Alcor'

    # apply calculations such as getting coordinates and color 
    df = star_data_calculator(df, ordered_star_names)

    # viewing angle and title for gif and png
    view = (-43, -2)
    title = 'big_dipper'

    # plots the Big Dipper asterism
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, df.common_name.values, title=title, view=view)

    return title, fig, ax, view

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

    # find little dipeper stars in the df
    df = df[df['alt_name'].isin(little_dipper_stars)]

    # map alternative names to common names
    name_mapping = dict(zip(little_dipper_stars, ordered_star_names))

    # apply mapping
    df['common_name'] = df['alt_name'].map(name_mapping)

    # apply calculations such as getting coordinates and color 
    df = star_data_calculator(df, ordered_star_names)

    title = 'little_dipper'
    view = (29, -135)

    # plots the Little Dipper asterism
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, df.common_name.values, title=title, view=view)

    return title, fig, ax, view

def summer_triangle():

    # current directory
    current_dir = os.path.dirname('src')

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', 'data_j2000.csv')

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    # check if types are correct and convert if otherwise
    df = check_and_convert_types(df)

    # Summer Triangle stars in Ursa Minor, alternative names and common names respectivly
    summer_triangle_stars = ['53Alp Aql', '50Alp Cyg', '3Alp Lyr']
    ordered_star_names = ['Altair', 'Deneb', 'Vega']
    
    # find summer triangle stars in the df
    df = df[df['alt_name'].isin(summer_triangle_stars)]

    # map alternative names to common names
    name_mapping = dict(zip(summer_triangle_stars, ordered_star_names))

    # apply mapping 
    df['common_name'] = df['alt_name'].map(name_mapping)

    # apply calculations such as getting coordinates and color 
    df = star_data_calculator(df, ordered_star_names)

    title = 'summer_triangle'
    view = (29, -135)

    # plots the Summer Triangle asterism
    fig, ax, view = plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, df.common_name.values, title=title, view=view)

    return title, fig, ax, view
