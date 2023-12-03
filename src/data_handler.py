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

def convert_ra_to_deg(ra):
    # Split the string into hours, minutes, and seconds
    parts = ra.split()
    if len(parts) != 3:
        return None  # Handle invalid format
    hours, minutes, seconds = map(float, parts)
    # Convert to degrees
    return 15 * (hours + minutes/60 + seconds/3600)


def convert_dec_to_deg(dec):
    # Split the string into degrees, arcminutes, and arcseconds
    parts = dec.split()
    if len(parts) != 3:
        return None  # Handle invalid format
    degrees, arcminutes, arcseconds = map(float, parts)
    # Convert to decimal degrees
    return degrees + arcminutes/60 + arcseconds/3600

def get_data_frame(file):

    # current directory
    current_dir = os.path.dirname('src')

    # directory of data relative to current directory
    data_file_path = os.path.join(current_dir, '..', 'data', file)

    # load data from csv to pandas dataframe
    df = load_data(data_file_path)

    df = standard_hr_column(df)

    return df

def get_dictionary(file_name):
    # Get the current directory 
    current_dir = os.getcwd()

    # Construct the file path to the Python file
    file_path = os.path.join(current_dir, '..', 'data', f'{file_name}.py')

    # Add the directory containing the Python file to sys.path
    sys.path.append(os.path.dirname(file_path))

    # Import the module using its filename
    module = __import__(file_name)

    # Extract the dictionary with the same name as the file
    if file_name in module.__dict__:
        return module.__dict__[file_name]
    else:
        raise ImportError(f"{file_name} dictionary not found in the specified module")

from calculations import star_data_calculator
from helper import greek_letter

def results_to_csv():
    # Load and join dataframes
    df = join_simbad()
    df2 = get_data_frame('iau_star_names.csv')

    # Join df and df2, including specific columns from df2
    df = df.merge(df2[['hr', 'Origin', 'Etymology Note', 'Source']], 
                  on='hr',  how='left', suffixes=('_simbad', '_iau'))

    # Rename columns
    df.rename(columns={'Origin': 'origin', 'Etymology Note': 'note', 'Source': 'source'}, inplace=True)

    # Get constellation names dictionary
    constellation_names = get_dictionary('constellation_names')

    constellation_data_array = []

    for common_name, alt_name in constellation_names.items():
        # Filter dataframe for stars in the current constellation
        mask = df['alt_name'].str.contains(alt_name, na=False)
        df_filtered = df[mask]

        # Special processing for certain constellations
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
        file.write('format object f1 "%IDLIST(HR),%COO(A),%COO(D),%PLX(V)"\n')
        for row in df.hr:
            file.write(f'query id HR {row}\n')

import csv

def standard_hr_column(df):

    df['hr'] = df['hr'].str.strip()
    df['hr'] = df['hr'].str.replace(' ', '')

    return df

def join_simbad():

    # Load data from CSV files
    df_ysb = get_data_frame('data_j2000.csv')
    df_simbad = get_data_frame('simbad_results.csv')
    df_iau = get_data_frame('iau_star_names.csv')

    df_iau.rename(columns={'IAU Name ' : 'iau_name', 'Origin' : 'origin', 'Etymology Note' : 'note', 'Source' : 'source'}, inplace=True)

    df_simbad['ra'] = df_simbad.apply(lambda row: convert_ra_to_deg(row['ra']), axis=1)
    df_simbad['dec'] = df_simbad.apply(lambda row: convert_dec_to_deg(row['dec']), axis=1)
    
    update = df_ysb[df_ysb['hr'] == 7539].index

    # Merge the two DataFrames on 'hr' column with suffixes
    combined_df = pd.merge(df_ysb, df_simbad, on='hr', how='inner', suffixes=('_ysb', '_simbad'))
    combined_df = pd.merge(combined_df, df_iau[['hr', 'iau_name']], on='hr', how='left')

    # Handling missing parallax values
    combined_df['parallax_simbad'] = combined_df['parallax_simbad'].replace('~ ', 0)
    combined_df['parallax_simbad'] = combined_df['parallax_simbad'].astype(float)

    # hr 1948 doenst have a parallax_simbad value so using parallax_ysb instead
    combined_df.loc[combined_df['hr'] == 'HR1948', 'parallax_simbad'] = combined_df.loc[combined_df['hr'] == 'HR1948', 'parallax_ysb'] * 1000

    # Save the combined DataFrame
    combined_df.to_csv('../data/joined_simbad.csv', index=False)

    return combined_df
