import os
import pandas as pd

current_dir = os.path.dirname('data_handler.py')
data_file_path = os.path.join(current_dir, '..', 'data', 'bsc5.dat')

colspecs = [
        (0, 4),     # Col 1: ID
        (5, 19),    # Col 2: Star names
        (20, 30),   # Col 3: 

]

column_names = ['id', 'star_name', 'code']

df = pd.read_fwf(data_file_path, colspecs=colspecs, names=column_names)

print(df.star_name.head())
