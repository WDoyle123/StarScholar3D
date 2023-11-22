from big_dipper import big_dipper
from little_dipper import little_dipper
from summer_triangle import summer_triangle
from all_stars import all_stars
from plotter import capture_gif


# call functions to plot all stars in the data
print('all_stars')
#title, fig, ax, view = all_stars()
print('creating animation...')
#capture_gif(title, fig, ax, view)

# call functions to plot stars in the big dipper asterism
print('big dipper')
#title, fig, ax, view = big_dipper()
print('capturing animation...')
#capture_gif(title, fig, ax, view)

# call function to plot stars in the little dipper asterism
#title, fig, ax, view = little_dipper()
#capture_gif(title, fig, ax, view)

title, fig, ax, view = summer_triangle()
capture_gif(title, fig, ax, view)
