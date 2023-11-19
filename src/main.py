import os
import pandas

from data_handler import load_data, check_and_convert_types
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate

# current directory
current_dir = os.path.dirname('src')

# directory of data relative to current directory
data_file_path = os.path.join(current_dir, '..', 'data', 'raw_data.csv')

# load data from csv to pandas dataframe
df = load_data(data_file_path)

# check if types are correct and convert if otherwise
df = check_and_convert_types(df)

# remove any NaN and zero values found in parallax column
df = df[(df['parallax'].notna() & df.parallax != 0)]

x_coordinates_array = []    # store x-coordinates
y_coordinates_array = []    # store y-coordinates
z_coordinates_array = []    # store z-coordinates

# loop through data frame and calculate x, y, z coordinates from the data
for index, row in df.iterrows():

    # calculate distance (parsecs) using parallax (note: parallax in arcseconds)
    distance = calculate_distance(row['parallax'])
   
    # calculate cartesian coordinates 
    x_coordinate = calculate_x_coordinate(distance, row['dec'], row['ra'])
    y_coordinate = calculate_y_coordinate(distance, row['dec'], row['ra'])
    z_coordinate = calculate_z_coordinate(distance, row['dec'])
    
    # append arrays with cartesian coordinates
    x_coordinates_array.append(x_coordinate)
    y_coordinates_array.append(y_coordinate)
    z_coordinates_array.append(z_coordinate)

