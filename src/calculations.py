import numpy as np

def calculate_distance(parallax):
    '''
    calculates distance in parsecs if parallax is in arcseconds
    '''
    return 1 / parallax

def calculate_x_coordinate(distance, declination, right_ascension):
    '''
    calculate x coordinate in cartesian space
    '''
    return distance * np.cos(declination) * np.sin(right_ascension)

def calculate_y_coordinate(distance, declination, right_ascension):
    '''
    calculate y coordinate in cartesian space
    '''
    return distance * np.sin(declination) * np.cos(right_ascension)

def calculate_z_coordinate(distance, declination):
    '''
    calculate z coordinate in cartesian space
    '''
    return distance * np.sin(declination)
