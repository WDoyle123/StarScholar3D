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
