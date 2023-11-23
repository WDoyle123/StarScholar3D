from asterisms import big_dipper, little_dipper, summer_triangle
from constellations import ursa_major, ursa_minor
from plotter import capture_gif

from matplotlib import pyplot as plt

# call functions to plot stars in the big dipper asterism
title, fig, ax, view = big_dipper()
print(f'{title}')
#capture_gif(title, fig, ax, view)

# call function to plot stars in the little dipper asterism
title, fig, ax, view = little_dipper()
#capture_gif(title, fig, ax, view)
print(f'{title}')

title, fig, ax, view = summer_triangle()
#capture_gif(title, fig, ax, view)
print(f'{title}')

title, fig, ax, view = ursa_major()
#capture_gif(title, fig, ax, view)
print(f'{title}')

title, fig, ax, view = ursa_minor()
#capture_gif(title, fig, ax, view)
print(f'{title}')
plt.show()

