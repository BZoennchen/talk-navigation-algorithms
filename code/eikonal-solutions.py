import skfmm
import numpy as np
import pylab as plt
import seaborn as sns
from matplotlib.colors import ListedColormap


def plot_contours(X, Y, Z, levels, title="Reisezeit", filename="reisezeit.pdf", phi=None):
    plt.figure(figsize=(10, 5))
    plt.title(title)
    plt.contourf(X, Y, Z, levels, cmap=ListedColormap(
        sns.color_palette("coolwarm", levels).as_hex()))
    plt.colorbar()
    plt.contour(X, Y, Z, levels, colors='black')
    if phi is not None:
        plt.contour(X, Y, phi, [0], linewidths=(3), colors='black')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_speed(X, Y, Z, levels, filename="reisegeschwindigkeit.pdf", phi=None):
    plt.figure(figsize=(10, 5))
    plt.title("Reisegeschwindigkeit")
    plt.contourf(X, Y, Z, levels, cmap=ListedColormap(
        sns.color_palette("vlag", levels).as_hex()))
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_simple_example():
    levels = 20
    X, Y = np.meshgrid(np.linspace(-1, 1, 401), np.linspace(-1, 1, 401))
    phi = -1*np.ones_like(X)
    phi[X > -0.5] = 1
    phi[np.logical_and(np.abs(Y) < 0.25, X > -0.75)] = 1
    plt.contour(X, Y, phi, [0], linewidths=(3), colors='black')
    plt.title('Boundary location: the zero contour of phi')
    plt.savefig('2d_phi.png')
    plt.show()
    d = skfmm.distance(phi, dx=1e-2)
    plot_contours(X, Y, d, levels, phi=phi)
    speed = np.ones_like(X)
    speed[Y > 0] = 1.5
    t = skfmm.travel_time(phi, speed, dx=1e-2)
    plot_contours(X, Y, t, levels, phi=phi)


def plot_hole():
    levels = 20
    X, Y = np.meshgrid(np.linspace(-2, 2, 401), np.linspace(-1, 1, 201))

    # define destination
    phi = 1*np.ones_like(X)
    phi[X > 1.9] = 0

    # define travel speed function
    speed = np.ones_like(X)
    speed[obstacle_distance(X, Y) <= 0] = 0
    d = skfmm.travel_time(phi, speed, dx=1e-2)
    plot_contours(X, Y, d, levels, phi=phi, filename="reisezeit-hindernis.pdf")


def plot_hole_lowed():
    levels = 20
    X, Y = np.meshgrid(np.linspace(-2, 2, 401), np.linspace(-1, 1, 201))

    # define destination
    phi = 1*np.ones_like(X)
    phi[X > 1.9] = 0

    # define travel speed function
    speed = np.ones_like(X)
    dist = np.maximum(0, obstacle_distance(X, Y))
    speed = 1 / (2 - np.minimum(1, dist/0.2))
    #speed = np.maximum(0.1, np.minimum(1, dist/0.2))
    #speed = dist
    speed[obstacle_distance(X, Y) <= 0] = 0
    d = skfmm.travel_time(phi, speed, dx=1e-2)
    plot_contours(X, Y, d, levels, phi=phi,
                  filename="reisezeit-hindernis-verlangsamung.pdf")
    plot_speed(X, Y, speed, levels,
               filename="reisegeschwindigkeit-hindernis-verlangsamung.pdf")


def obstacle_distance(X, Y):
    return np.maximum(np.abs(X)-0.8, np.abs(Y)-0.5)


def main():
    # plot_simple_example()
    plot_hole()
    plot_hole_lowed()


if __name__ == '__main__':
    main()
