from asterisms import big_dipper, little_dipper, summer_triangle, orions_belt, cassiopeia_w
from constellations import ursa_major, ursa_minor, cassiopeia
from all_stars import all_stars
from plotter import capture_gif

from matplotlib import pyplot as plt

# flags for toggling gif capture and plot display
capture_gif_flag = False
show_plot_flag = True

# flags for processing asterisms and constellations
process_asterisms = True
process_constellations = True
process_all_stars = False

# lists of functions for asterisms and constellations#
asterism_functions = [big_dipper, little_dipper, summer_triangle, orions_belt, cassiopeia_w]

#asterism_functions = [big_dipper] # for testing

constellation_functions = [ursa_major, ursa_minor, cassiopeia]

# combine lists based on flags
celestial_objects = []
if process_asterisms:
    celestial_objects.extend(asterism_functions)
if process_constellations:
    celestial_objects.extend(constellation_functions)
if process_all_stars:
    celestial_objects.append(all_stars)

# processing loop
for celestial_object in celestial_objects:
    title, fig, ax, view = celestial_object()
    print(f'{title}')

    if capture_gif_flag:
        capture_gif(title, fig, ax, view)

    if show_plot_flag:
            plt.show()
            plt.close(fig)
