from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio
import io
import cv2
import numpy as np

def plot_3d_scatter(x, y, z, rgb, star_names=None, title=None, view=None):
    '''
    Creates a 3D plot using Cartesian coordinates with a black background,
    white points, grey axes, and black grid panes.
    '''
    # create figure
    fig = plt.figure(figsize=(10, 8))
    fig.set_facecolor('black')

    # create 3d projection
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

    # create scatter plot on the 3d projection
    scatter = ax.scatter(x, y, z, color=rgb, s=15)

    # add annotations if star names are provided
    if star_names is not None:
        for i in range(len(x)):
            ax.text(x[i], y[i], z[i], star_names[i], color='white', fontsize=9)

        # joins the two stars by a line, completing the drawing of the asterism
        if 'Phecda' in star_names and 'Megrez' in star_names:
            star_names_list = list(star_names)
            index_phecda = star_names_list.index('Phecda')
            index_megrez = star_names_list.index('Megrez')
            
            # plots line
            ax.plot([x[index_phecda], x[index_megrez]],
                    [y[index_phecda], y[index_megrez]],
                    [z[index_phecda], z[index_megrez]],
                    color='white', linewidth=1)

        # draw lines connecting the stars in the Big Dipper
        ax.plot(x, y, z, color='white', linewidth=1)

    # set labels with grey color
    ax.set_xlabel('X Coordinate', color='grey')
    ax.set_ylabel('Y Coordinate', color='grey')
    ax.set_zlabel('Z Coordinate', color='grey')

    # use title from function call or default
    if title is not None:
        ax.set_title(title, color='white',fontsize=18, pad=20)
    else:
        ax.set_title('3D Star Map', color='white',fontsize=18, pad=20)

    # set tick colors to grey
    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')
    ax.tick_params(axis='z', colors='grey')

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
        ax.view_init(45, 45)

    # show plot
    #    plt.show()
    return fig, ax

def img_from_fig(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def capture_gif(fig, ax):
    fps = 20
    pause_duration_sec = 5
    pause_frames = pause_duration_sec * fps
    initial_img = img_from_fig(fig)
    initial_img_pause = initial_img * pause_frames
    frames = []
    frames.append(initial_img_pause)
    for angle in range(0, 360, 1):
        ax.view_init(30, angle)
        img = img_from_fig(fig)
        frames.append(img)
    imageio.mimsave('plot_new.gif', frames, fps=fps)
