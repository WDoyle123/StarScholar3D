import os
import pandas as pd

from data_handler import load_data, check_and_convert_types
from calculations import calculate_distance, calculate_x_coordinate, calculate_y_coordinate, calculate_z_coordinate, bv_color_to_rgb
from plotter import plot_3d_scatter

# current directory
current_dir = os.path.dirname(__file__)  # Corrected to get the actual script directory

# directory of data relative to current directory
data_file_path = os.path.join(current_dir, '..', 'data', 'data.csv')

# load data from csv to pandas dataframe
df = load_data(data_file_path)

# check if types are correct and convert if otherwise
df = check_and_convert_types(df)

# Big Dipper stars in Ursa Major
big_dipper_stars = ['79Zet UMa', '77Eps UMa', '69Del UMa', '64Gam UMa', '48Bet UMa', '50Alp UMa']
ordered_star_names = ['Mizar A', 'Mizar B', 'Alioth', 'Megrez', 'Dubhe', 'Merak', 'Phecda']

# filter the df to include only the Big Dipper stars
df = df[df['alt_name'].isin(big_dipper_stars)]

# Map alternative names to common names
name_mapping = {
    '79Zet UMa': 'Mizar',
    '77Eps UMa': 'Alioth',
    '69Del UMa': 'Megrez',
    '64Gam UMa': 'Phecda',
    '48Bet UMa': 'Merak',
    '50Alp UMa': 'Dubhe'
}
df['common_name'] = df['alt_name'].map(name_mapping)

# Manually adjust the entries for Mizar A and Mizar B
mizar_a_coords = (113.11073, 61.57916)
mizar_b_coords = (113.10430, 61.58205)

for index, row in df.iterrows():
    if row['alt_name'] == '79Zet UMa':
        coords = (row['ra'], row['dec'])
        if coords == mizar_a_coords:
            df.at[index, 'common_name'] = 'Mizar A'
        elif coords == mizar_b_coords:
            df.at[index, 'common_name'] = 'Mizar B'

df['common_name'] = pd.Categorical(df['common_name'], categories=ordered_star_names, ordered=True)
df = df.sort_values(by='common_name')

# remove any NaN and zero values found in parallax column
df = df[(df['parallax'].notna() & df.parallax != 0)]

# Calculate x, y, z coordinates and RGB colors, and add them to the DataFrame
df['distance'] = df.apply(lambda row: calculate_distance(row['parallax']), axis=1)
df['x_coordinate'] = df.apply(lambda row: calculate_x_coordinate(calculate_distance(row['distance']), row['dec'], row['ra']), axis=1)
df['y_coordinate'] = df.apply(lambda row: calculate_y_coordinate(calculate_distance(row['distance']), row['dec'], row['ra']), axis=1)
df['z_coordinate'] = df.apply(lambda row: calculate_z_coordinate(calculate_distance(row['distance']), row['dec']), axis=1)
df['rgb_color'] = df['bv_color'].apply(bv_color_to_rgb)

print(df)

plot_3d_scatter(df.x_coordinate.values, df.y_coordinate.values, df.z_coordinate.values, df.rgb_color.values, df.common_name.values)
