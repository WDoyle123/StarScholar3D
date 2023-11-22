from asterisms import big_dipper, little_dipper, summer_triangle
from plotter import capture_gif

# call functions to plot stars in the big dipper asterism
print('big dipper')
title, fig, ax, view = big_dipper()
print('capturing animation...')
#capture_gif(title, fig, ax, view)

# call function to plot stars in the little dipper asterism
title, fig, ax, view = little_dipper()
#capture_gif(title, fig, ax, view)

title, fig, ax, view = summer_triangle()
#capture_gif(title, fig, ax, view)
