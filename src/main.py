from asterisms import *
from constellations import *
from all_stars import all_stars
from plotter import capture_gif
from data_handler import results_to_csv

from matplotlib import pyplot as plt

# flags for toggling gif capture and plot display
capture_gif_flag = True
show_plot_flag = False

# flags for processing asterisms and constellations
process_asterisms = True
process_constellations = False
process_all_stars = False

# lists of functions for asterisms and constellations#
asterism_functions = [big_dipper, little_dipper, summer_triangle, orions_belt, cassiopeia_w]

#asterism_functions = [big_dipper] # for testing

# combine lists based on flags
celestial_objects = []
if process_asterisms:
    celestial_objects.extend(asterism_functions)
if process_constellations:
    constellations(plot=show_plot_flag, gif=capture_gif_flag)
if process_all_stars:
    celestial_objects.append(all_stars)

# processing loop
for celestial_object in celestial_objects:
    title, fig, ax, view = celestial_object()
    print(f'{title}')

    if capture_gif_flag:
        capture_gif(title, fig, ax, view, of_type='asterism')

    if show_plot_flag:
            plt.show()
            plt.close(fig)

# get results in csv format
#results_to_csv()
