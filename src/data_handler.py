import os
import pandas as pd

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

