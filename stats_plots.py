import matplotlib.pyplot as plt

def plot_scatter_players(players,x,y,labelx,labely,titol,color_players):

    fig = plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color=color_players)

    for i, player in enumerate(players):
        # if (x[i] != 0) and (y[i] != 0):
        plt.annotate(player, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center',fontsize=8)

    plt.grid(True, linestyle='--', alpha=0.3)

    # Label the axes
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(titol)
    
    # plt.axhline(mean_y, color='black', linestyle='--', linewidth=1, label='Avg')
    # plt.axvline(mean_x, color='black', linestyle='--', linewidth=1, label='Avg')


    # Show the plot
    plt.tight_layout()
    plt.show()
    return fig