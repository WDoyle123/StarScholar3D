import numpy as np
import pandas as pd
import math

def star_data_calculator(df, ordered_star_names=None):

    # avoid settingwithcopywarning from pandas
    df = df.copy()    

    # remove any NaN and zero values found in parallax column
    df = df[(df['parallax_simbad'].notna() & df.parallax_simbad != 0)]
    
    # Replace NaN values in 'bv_color' with 0.5
    df['bv_color'] = df['bv_color'].fillna(0.5)

    df['star_size'] = df.apply(lambda row: assign_star_size(row['vmag']), axis=1)

    # turns degrees to radians (np.sin and np.cos already do this but this will update the df)
    df['dec_simbad'] = df.apply(lambda row: degrees_to_radians(row['dec_simbad']), axis=1)
    df['ra_simbad'] = df.apply(lambda row: degrees_to_radians(row['ra_simbad']), axis=1)

    # Calculate x, y, z coordinates and RGB colors, and add them to the df
    df['distance'] = df.apply(lambda row: calculate_distance(row['parallax_simbad']), axis=1)

    if ordered_star_names is not None:
        # create order to the stars, this allows for connecting the stars using a line plot in plotter.py
        df['common_name'] = pd.Categorical(df['common_name'], categories=ordered_star_names, ordered=True)
        df = df.sort_values(by='common_name')

    # create x y z coordinates in the df using distance, declination and right acension
    df['x_coordinate'] = df.apply(lambda row: calculate_x_coordinate((row['distance']), row['dec_simbad'], row['ra_simbad']), axis=1)
    df['y_coordinate'] = df.apply(lambda row: calculate_y_coordinate((row['distance']), row['dec_simbad'], row['ra_simbad']), axis=1)
    df['z_coordinate'] = df.apply(lambda row: calculate_z_coordinate((row['distance']), row['dec_simbad']), axis=1)

    # creates a color variable to each star (approximatly)
    df['rgb_color'] = df['bv_color'].apply(lambda row: bv_color_to_rgb(row))

    return df

def degrees_to_radians(degree):
    '''
    turns the degrees to radians
    '''
    return degree * (np.pi / 180)

def calculate_distance(parallax):
    '''
    calculates distance in parsecs if parallax is in arcseconds
    '''
    # convert to arc seconds from milli arc seconds
    parallax = parallax / 1000
    return 1 / parallax

# source for calculating x,y,z https://www.jameswatkins.me/posts/converting-equatorial-to-cartesian.html

def calculate_x_coordinate(distance, declination, right_ascension):
    '''
    calculate x coordinate in cartesian space
    '''
    return distance * np.cos(declination) * np.cos(right_ascension)

def calculate_y_coordinate(distance, declination, right_ascension):
    '''
    calculate y coordinate in cartesian space
    '''
    return distance * np.cos(declination) * np.sin(right_ascension)

def calculate_z_coordinate(distance, declination):
    '''
    calculate z coordinate in cartesian space
    '''
    return distance * np.sin(declination)

def bv_to_temperature(bv):
    '''
    calculates the temperature of the star using the bv color 
    following: https://arxiv.org/abs/1201.1809 using equation (14)

    '''
    return 4600 * ((1 / (0.92 * bv + 1.7)) + (1 / (0.92 * bv + 0.62)))

def temperature_to_rgb(temperature):

    # normalize temperature
    # 3500K for cooler stars
    # 7500K for hotter stars
    norm_temp = (temperature - 3500) / (7500 - 3500)

    # keep norm between 0 and 1
    norm_temp = max(0.0, min(norm_temp, 1.0))

    # color transition: red -> orange -> yellow -> white -> light blue -> blue
    if norm_temp < 0.2:
        # red to orange
        r = 1.0
        g = norm_temp / 0.2
        b = 0
    elif norm_temp < 0.4:
        # orange to yellow
        r = 1.0
        g = 0.5 + 0.5 * ((norm_temp - 0.2) / 0.2)
        b = 0
    elif norm_temp < 0.6:
        # yellow to white
        r = 1.0
        g = 1.0
        b = (norm_temp - 0.4) / 0.2
    elif norm_temp < 0.8:
        # white to light blue
        r = 1.0 - ((norm_temp - 0.6) / 0.2)
        g = 1.0
        b = 1.0
    else:
        # light blue to blue
        r = 0
        g = 1.0 - ((norm_temp - 0.8) / 0.2)
        b = 1.0

    return (r, g, b)

def bv_color_to_rgb(bv_color):
    '''
    turn bv color into visible color for illustrative purpuses using approximations
    '''
    temperature = bv_to_temperature(bv_color)
    return temperature_to_rgb(temperature)

def assign_star_size(vmag):
    if vmag < 2:
        size = 100  # Largest size for the brightest stars
    elif vmag < 3:
        size = 50
    elif vmag < 4:
        size = 25
    elif vmag < 5:
        size = 13
    elif vmag < 6:
        size = 6
    else:
        size = 3  # Smaller size for fainter stars

    return size

def find_closest_star_view(df):

    # Find the row with the smallest distance value
    closest_star = df.loc[df['distance'].idxmin()]

    # Get the x, y, z coordinates of the closest star
    x, y, z = closest_star['x_coordinate'], closest_star['y_coordinate'], closest_star['z_coordinate']

    # Calculate the azimuth and elevation angles for the view with origin (0, 0)
    azimuth = np.degrees(np.arctan2(y, x)) % 360
    elevation = np.degrees(np.arctan2(z, np.sqrt(x**2 + y**2)))

    # Adjust the azimuth to face the star directly
    azimuth = (azimuth + 180) % 360
    if azimuth > 180:  # Adjust azimuth to the range (-180, 180)
        azimuth -= 360

    # Make sure elevation is in the range (-90, 90) avoid inversion
    elevation = max(min(elevation, 90), -90)

    return elevation, azimuth
