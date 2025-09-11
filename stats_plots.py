import matplotlib.pyplot as plt

def plot_scatter_players(players,x,y,labelx,labely,titol,color_players):

    fig = plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color=color_players)

    # Regression line
    import numpy as np
    x_np = np.array(x)
    y_np = np.array(y)
    if len(x_np) > 1:
        coeffs = np.polyfit(x_np, y_np, 1)
        x_line = np.linspace(x_np.min(), x_np.max(), 100)
        reg_y = coeffs[0] * x_line + coeffs[1]
        plt.plot(x_line, reg_y, color='black', linestyle='--', linewidth=0.7, alpha=0.5)

    for i, player in enumerate(players):
        plt.annotate(player, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center',fontsize=8)

    plt.grid(True, linestyle='--', alpha=0.3)

    # Label the axes
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(titol)

    plt.tight_layout()
    plt.show()
    return fig