from asterisms import *
from constellations import *
from all_stars import all_stars
from plotter import capture_gif
from data_handler import results_to_csv, query_simbad, join_simbad

def main():

    # Flags for toggling GIF capture and plot display
    capture_gif_flag = True  # Set to True to enable GIF capture, False to disable
    show_plot_flag = False   # Set to True to display plots, False to hide them

    # Flags for processing different astronomical features
    process_asterisms = True       # Set to True to process asterisms, False to skip
    process_constellations = True  # Set to True to process constellations, False to skip
    process_all_stars = True       # Set to True to process all stars, False to skip

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

    results_to_csv()

if __name__ == '__main__':
    main()
