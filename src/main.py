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
process_constellations = False
process_all_stars = False

# lists of functions for asterisms and constellations#
asterism_functions = [big_dipper, little_dipper, summer_triangle, orions_belt, cassiopeia_w]

#asterism_functions = [big_dipper] # for testing

if process_all_stars:
    print('all_stars')
    title, fig, ax, view = all_stars()

    if capture_gif_flag:
        capture_gif(title, fig, ax, view, of_type='constellation')

    if show_plot_flag:
        plt.show()
        plt.close(fig)

if process_asterisms:
    print("Starting asterism processing...")

    start_time = time.time()
    counter = 0
    len_of_df = len(asterism_functions)

    for asterism in asterism_functions:
        title, fig, ax, view = asterism()

        if capture_gif_flag:
            capture_gif(title, fig, ax, view, of_type='asterism')

        if show_plot_flag:
            plt.show()
            plt.close(fig)

        counter += 1

        # Calculate the percentage and the elapsed time
        percent_complete = (counter / len_of_df) * 100
        elapsed_time = time.time() - start_time

        # Estimate remaining time
        if counter > 0:
            remaining_time = (elapsed_time / counter) * (len_of_df - counter)
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            print(f'\rAsterism Progress: {percent_complete:.2f}% complete - Time remaining: {remaining_minutes}m {remaining_seconds}s', end='', flush=True)
        else:
            print(f'\rAsterism Progress: {percent_complete:.2f}% complete - Time remaining: estimating...', end='', flush=True)

    # After the loop, print the total time taken
    total_time = time.time() - start_time
    total_minutes = int(total_time // 60)
    total_seconds = int(total_time % 60)
    print(f"\nAll asterisms processed! Total time: {total_minutes}m {total_seconds}s")

if process_constellations:
    constellations(plot=show_plot_flag, gif=capture_gif_flag)

# get results in csv format

results_to_csv()
#query_simbad()

