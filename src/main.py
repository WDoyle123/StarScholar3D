from big_dipper import big_dipper
from all_stars import all_stars
from plotter import capture_gif

# call functions to plot all stars in the data
#all_stars()

# call functions to plot stars in the big dipper asterism
fig, ax = big_dipper()
capture_gif(fig, ax)
