from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_scatter(x, y, z, rgb):
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
    ax.scatter(x, y, z, color=rgb, s=15)

    # set labels and title with grey color
    ax.set_xlabel('X Coordinate', color='grey')
    ax.set_ylabel('Y Coordinate', color='grey')
    ax.set_zlabel('Z Coordinate', color='grey')
    ax.set_title('3D Star Map', color='grey')

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
    ax.view_init(30, 60)

    # show plot
    plt.show()
    return None

