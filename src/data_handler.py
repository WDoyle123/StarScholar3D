import os
import sys
import pandas as pd
import numpy as np

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
        else:
            print(f"Column {column} not found in DataFrame")

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

def get_common_names():
    # get the current directory 
    current_dir = os.path.dirname('src')

    # Construct the file path to 'constellation_names.py'
    file_path = os.path.join(current_dir, '..', 'data', 'constellation_names.py')

    # Add the directory containing 'constellation_names.py' to sys.path
    sys.path.append(os.path.dirname(file_path))

    # Import 'common_names' from 'constellation_names'
    from constellation_names import common_names

    return common_names

def extract_constellations(df):

    data = df.alt_name
    data.replace('nan', np.nan, inplace=True)
    data.dropna(inplace=True)

    # filter out rows where the string length is less than the threshold
    filtered_data = data[data.str.len() >= 5]

    # extract the last three characters as constellation names
    filtered_data = filtered_data[filtered_data.str[-3:].str.isalpha()]

    # extracting constellation names
    constellations_array = filtered_data.str[-3:].unique()

    return constellations_array

def constellation_dictionary(df):

    # get both the alternative names and common names 
    alt_names = extract_constellations(df)
    common_names = get_common_names()

    # create a dictionary eg. UMi : Ursa Minor
    constellation_names = dict(zip(alt_names, common_names))

    return constellation_names

