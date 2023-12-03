from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio
import io
import cv2
import numpy as np
import os
from PIL import Image
import pandas as pd

def draw_line_between_stars(ax, star_names, star_coords, star1, star2, color='white', linewidth=1):
    if star1 in star_names and star2 in star_names:
        star_names_list = list(star_names)
        index_star1 = star_names_list.index(star1)
        index_star2 = star_names_list.index(star2)

        ax.plot([star_coords['x'][index_star1], star_coords['x'][index_star2]],
                [star_coords['y'][index_star1], star_coords['y'][index_star2]],
                [star_coords['z'][index_star1], star_coords['z'][index_star2]],
                color=color, linewidth=linewidth)

def plot_3d_scatter(x, y, z, rgb, star_size, iau_names=None, title=None, view=None, lines=True, no_grid_lines=True, show_title=False):
 
    # create figure
    fig = plt.figure(figsize=(10, 8))
    fig.set_facecolor('black')

    # create 3d projection
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

    # create scatter plot on the 3d projection
    scatter = ax.scatter(x, y, z, color=rgb, s=star_size, alpha=1.0, depthshade=False)

    # add annotations if star names are provided
    if iau_names is not None:
        star_names_fontsize = 8
        for i in range(len(x)):
                name_to_plot = '' if pd.isna(iau_names[i]) else iau_names[i]
                ax.text(x[i], y[i], z[i], name_to_plot, color='white', fontsize=star_names_fontsize, alpha=0.75)

    # draw lines connecting the stars
    if lines == True:
        ax.plot(x, y, z, color='white', linewidth=1)
        
        star_names = [star for star in iau_names]

        # connect stars in a 'closed loop'
        star_coords = {'x': x, 'y': y, 'z': z}

        # for big dipper
        draw_line_between_stars(ax, star_names, star_coords, 'Phecda', 'Megrez')
    
        # for little dipper
        draw_line_between_stars(ax, star_names, star_coords, 'Eta UMi', 'Zet UMi')

        # for summer triangle
        draw_line_between_stars(ax, star_names, star_coords, 'Altair', 'Vega')

    # handling grid lines and axis labels
    if no_grid_lines:
        # hide axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')

        # hide tick labels
        for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
            axis.set_ticklabels([])
    
        # hide grid lines
        ax.grid(False)

        # hide tick labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        # hide the axes themselves
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.zaxis.set_visible(False)
    else:
        # set labels with grey color
        ax.set_xlabel('X Coordinate', color='grey')
        ax.set_ylabel('Y Coordinate', color='grey')
        ax.set_zlabel('Z Coordinate', color='grey')

    # set tick colors to grey
    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')
    ax.tick_params(axis='z', colors='grey')

    # use title from function call or default
    if show_title == True:
        ax.set_title(title, color='white',fontsize=18, pad=20)

    # set pane colors to black (make them blend with the background)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')

    # viewing angle (elevation, azimuth)
    if view is not None:
        ax.view_init(view[0], view[1])
    else:
        view = (45, 45)
        ax.view_init(view[0], view[1])

    # path to figures directory
    figures_directory = os.path.join('..', 'figures')
    
    # makes figures directory if it doesnt already exist
    if not os.path.exists(figures_directory):
        os.makedirs(figures_directory)

    # creates the figure file
    figures_path = os.path.join(figures_directory, f'{title}_plot.png')

    # saves the plot to the figures file
    fig.savefig(figures_path, bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=180)
    
    return fig, ax, view

def img_from_fig(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=90)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def capture_gif(title, fig, ax, start_view, of_type):

    #########################################
    # RAM INTENSIVE MIGHT CRASH YOUR TERMINAL
    #########################################

    # frames per second
    fps = 30
    
    if of_type == 'asterism':

        pause_duration_sec = 2

        pause_frames = int(pause_duration_sec * fps)

        initial_img = img_from_fig(fig)

        frames = [initial_img for _ in range(pause_frames)]

        ax.view_init(elev=start_view[0], azim=start_view[1])
        img = img_from_fig(fig)
        frames.append(img)

        start_elev, start_azim = start_view
        end_elev = 30

        # find the amount of steps needed for transition
        steps_elev = abs(end_elev - start_elev)
        for step in range(steps_elev + 1):
            # example halfway: elev = = -42 + (30 - (-42)) * 36 / 72 = -6
            elev = start_elev + (end_elev - start_elev) * step / steps_elev
            ax.view_init(elev=elev, azim=start_azim)
            img = img_from_fig(fig)
            frames.append(img)
    
        # rotate 360 degrees
        for angle in range(start_azim, start_azim +  360, 1):
            ax.view_init(elev=30, azim=angle)
            img = img_from_fig(fig)
            frames.append(img)

        # transistion to start_elev
        for step in range(steps_elev + 1):
            elev = end_elev + (start_elev - end_elev) * step / steps_elev
            ax.view_init(elev=elev, azim=start_azim)
            img = img_from_fig(fig)
            frames.append(img)

    if of_type == 'constellation' or title == 'all_stars':

        frames = []

        for angle in range(0, 360, 1):
            ax.view_init(elev=30, azim=angle)
            img = img_from_fig(fig)
            frames.append(img)

    # path to animations directory
    animations_directory = os.path.join('..', 'animations')
    animations_constellations_directory = os.path.join(animations_directory, 'constellations')
    animations_asterisms_directory = os.path.join(animations_directory, 'asterisms')

    # create directory if it does not exist
    if not os.path.exists(animations_directory):
        os.makedirs(animations_directory)
    if not os.path.exists(animations_constellations_directory):
        os.makedirs(animations_constellations_directory)
    if not os.path.exists(animations_asterisms_directory):
        os.makedirs(animations_asterisms_directory)

    if of_type == 'constellation':
        save_gif_to_directory = animations_constellations_directory
    if of_type == 'asterism':
        save_gif_to_directory = animations_asterisms_directory
    if title == 'all_stars':
        save_gif_to_directory = animations_directory

    # full file path
    gif_path = os.path.join(save_gif_to_directory, f'rotating_{title}.gif')

    # save frames as a gif with infinite loop
    imageio.mimsave(gif_path, frames, fps=fps, loop=0)
