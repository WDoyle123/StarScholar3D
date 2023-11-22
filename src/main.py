from big_dipper import big_dipper
from all_stars import all_stars
from plotter import capture_gif

# call functions to plot all stars in the data
print('all_stars')
title, fig, ax, view = all_stars()
print('creating animation...')
capture_gif(title, fig, ax, view)

# call functions to plot stars in the big dipper asterism
print('big dipper')
title, fig, ax, view = big_dipper()
print('capturing animation...')
capture_gif(title, fig, ax, view)
