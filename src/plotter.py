from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_scatter(x, y, z, rgb, star_names=None):
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
        if 'Phecda' in star_names and 'Megrez' in star_names:
            star_names_list = list(star_names)
            index_phecda = star_names_list.index('Phecda')
            index_megrez = star_names_list.index('Megrez')

            ax.plot([x[index_phecda], x[index_megrez]],
                    [y[index_phecda], y[index_megrez]],
                    [z[index_phecda], z[index_megrez]],
                    color='white', linewidth=1)

        # Draw lines connecting the stars in the Big Dipper
        # Ensure the stars are in the correct order for the Big Dipper
        ax.plot(x, y, z, color='white', linewidth=1)

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

