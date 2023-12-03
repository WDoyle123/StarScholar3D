from asterisms import *
from constellations import *
from all_stars import all_stars
from plotter import capture_gif
from data_handler import results_to_csv, query_simbad, join_simbad

from matplotlib import pyplot as plt

# flags for toggling gif capture and plot display
capture_gif_flag = True
show_plot_flag = False

# flags for processing asterisms and constellations
process_asterisms = True
process_constellations = True
process_all_stars = True

if process_all_stars:
    print('all_stars')
    title, fig, ax, view = all_stars()

    if capture_gif_flag:
        capture_gif(title, fig, ax, view, of_type='constellation')

    if show_plot_flag:
        plt.show()
        plt.close(fig)

if process_asterisms:
    asterisms(plot=show_plot_flag, gif=capture_gif_flag)

if process_constellations:
    constellations(plot=show_plot_flag, gif=capture_gif_flag)

