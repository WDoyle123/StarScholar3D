import os
import sys
import pandas as pd
import numpy as np
import regex as re

def load_data(file_path):
    '''
    Function used to load raw data into a pandas data frame
    '''
    # read the csv from specified file path
    df = pd.read_csv(file_path)
    return df

def check_and_convert_types(df):
    '''
    Check and expected variable type against the raw data's variable type and change when observed difference
    '''
    # dictionary containing the expected variable types
    expected_types = {
        'name': str,        # name should be string
        'alt_name': str,    # alt name should be string
        'ra': float,        # right assencion should be float
        'dec': float,       # declination should be float
        'bv_color': float,  # color (bv) should be float
        'parallax': float   # parallax should be float
    }

    # column and type in the expected types dictionary
    for column, expected_type in expected_types.items():
        # check if column exists in dataframe
        if column in df.columns:
            # check if column is the expected type
            if not pd.api.types.is_dtype_equal(df[column].dtype, expected_type):
                # convert column to the expected data type
                try:
                    df[column] = df[column].astype(expected_type)
                except ValueError as e:
                    print(f"Error converting {column}: {e}")
    return df

def get_data_frame(file):

    # current directory
    current_dir = os.path.dirname('src')

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', file)

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    # check if types are correct and convert if otherwise
    df = check_and_convert_types(df)

    return df

def get_constellation_dictionary():
    # get the current directory 
    current_dir = os.path.dirname('src')

    # Construct the file path to 'constellation_names.py'
    file_path = os.path.join(current_dir, '..', 'data', 'constellation_names.py')

    # Add the directory containing 'constellation_names.py' to sys.path
    sys.path.append(os.path.dirname(file_path))

    # Import 'common_names' from 'constellation_names'
    from constellation_names import constellation_abbreviations

    return constellation_abbreviations

from calculations import star_data_calculator
from helper import greek_letter

def results_to_csv():
    # Load the dataframes from CSV files
    df = join_simbad()
    df2 = get_data_frame('iau_star_names.csv')

    df.rename(columns={'hr' : 'name'}, inplace=True)

    df['name'] = 'HR ' + df['name'].astype(str)

    # Join df and df2 on 'Designation' in df2 and 'name' in df
    # Only include specific columns from df2
    df = df.merge(df2[['Designation', 'IAU Name ', 'Origin', 'Etymology Note', 'Source']], 
                  left_on='name', right_on='Designation', how='left')

    df.drop(columns=['Designation'], inplace=True)
    df.rename(columns={'IAU Name ' : 'iau_name', 'Origin' : 'origin', 'Etymology Note' : 'note', 'Source' : 'source'}, inplace=True)

    # Get constellation names dictionary
    constellation_names = get_constellation_dictionary()

    constellation_data_array = []

    for common_name, alt_name in constellation_names.items():
        # Filter dataframe for stars belonging to the current constellation
        mask = df['alt_name'].str.contains(alt_name, na=False)
        df_filtered = df[mask]

        # Special processing for specific constellations
        if alt_name in ['Del', 'Tau']:
            df_filtered = greek_letter(df_filtered, alt_name)

        # Calculate additional star data
        df_filtered = star_data_calculator(df_filtered)

        # Assign constellation names
        df_filtered['constellation_alt_name'] = alt_name
        df_filtered['constellation_common_name'] = common_name

        # Append to the main list
        constellation_data_array.append(df_filtered)

    # Combine all constellation data into a single dataframe
    result_df = pd.concat(constellation_data_array)

    # Save the combined dataframe to CSV
    result_df.to_csv('../data/all_constellations_and_their_stars.csv', index=False)

def query_simbad():
    df = get_data_frame('data_j2000.csv')

    with open('../data/query_simbad.txt', 'w') as file:
        file.write('format object form1 "%IDLIST(1) : %PLX(V)"\n')
        file.write('format display\n')
        for row in df.hr:
            file.write(f'query id HR {row}\n')

import csv

def join_simbad():
    index_counter = 1
    df = get_data_frame('data_j2000.csv')
 
    # Drop specific row
    index_to_drop = df[df['hr'] == 7539].index
    df = df.drop(index_to_drop)

    # Read and process data from text file
    parallax_values = []
    with open('../data/simbad_results.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            # Extract the part after the colon
            data = line.split(' : ')[1]
            parallax_values.append(data)

    # Create a DataFrame from the text file data
    df2 = pd.DataFrame({'parallax_simbad': parallax_values})

    # Merge the two DataFrames
    # Ensure that both df and df2 have the same number of rows
    combined_df = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)

    combined_df['parallax_simbad'] = combined_df['parallax_simbad'].replace('~', 0)

    combined_df['parallax_simbad'] = combined_df['parallax_simbad'].astype(float)

    # Save the combined DataFrame
    combined_df.to_csv('join_simbad.csv')

    return combined_df
