import uproot as up
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
import argparse
from os.path import join

CrystalLength = 52.5
CrystalWidth = 2.5
CrystalThick = 2.5
nLayer = 18
Bias = 0.5 * CrystalLength


def read_file(fname: str, tree:str, event_index: int):
    with up.open(fname) as f:
        tree = f[tree]
        Hit_X = tree['Hit_X'].array(library='np')
        Hit_Y = tree['Hit_Y'].array(library='np')
        Hit_Z = tree['Hit_Z'].array(library='np') / CrystalThick
        Hit_Energy = tree['Hit_Energy'].array(library='np')

        x = Hit_X[event_index]
        y = Hit_Y[event_index]
        z = np.round(Hit_Z[event_index]).astype(int)
        energy = Hit_Energy[event_index]

        return (x, y, z, energy)


def plot(fname: str, tree: str, event_index: int, title: str):
    x, y, z, energy = read_file(fname, tree, event_index)
    energy_norm = energy / np.max(energy)

    nhits = len(x)
    assert nhits == len(y)
    assert nhits == len(z)
    assert nhits == len(energy)

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    plt.gca().set_box_aspect((4 / 3, 1, 4 / 3))
    cmap = cm.OrRd

    for i in np.arange(nhits):
        if z[i] % 2 == 0:
            xnew = np.arange(x[i] - Bias, x[i] + 2 * CrystalLength - Bias, CrystalLength)
            ynew = np.arange(y[i], y[i] + 2 * CrystalWidth, CrystalWidth)
        else:
            xnew = np.arange(x[i], x[i] + 2 * CrystalWidth, CrystalWidth)
            ynew = np.arange(y[i] - Bias, y[i] + 2 * CrystalLength - Bias, CrystalLength)

        xnew, ynew = np.meshgrid(xnew, ynew)
        znew = z[i] * np.ones(xnew.shape)
        enew = energy_norm[i] * np.ones(xnew.shape)

        ax.plot_surface(xnew, znew, ynew, cmap=cmap, facecolors=cmap(enew), edgecolor='k', alpha=0.8, lw=0.05, rstride=1, cstride=1, antialiased=False)

    ax.set_xlim(-0.5 * CrystalLength, 0.5 * CrystalLength)
    ax.set_ylim(0, nLayer)
    ax.set_zlim(-0.5 * CrystalLength, 0.5 * CrystalLength)
    ax.set_xticks(np.linspace(-25, 25, 5))
    ax.set_yticks(np.arange(0, nLayer + 1, 3))
    ax.set_zticks(np.linspace(-25, 25, 5))
    ax.set_aspect(aspect='equalxz')
    ax.grid(False)

    fig.suptitle(title, size='xx-large')
    ax.invert_xaxis()
    ax.set_xlabel("X [cm]")
    ax.set_ylabel("Z [layer]")
    ax.set_zlabel("Y [cm]")

    m = plt.cm.ScalarMappable(cmap=cmap)
    m.set_array(energy)
    plt.colorbar(m, pad=0.2, label="Hit Energy [MeV]")

    ax.view_init(elev=25, azim=-40, roll=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", type=str, default='', required=True, help="Input ROOT file")
    parser.add_argument("-t", "--tree", type=str, default='dp', help="Input tree name (default: dp)")
    parser.add_argument("-i", "--title", type=str, default='', help="Title of display figure")
    parser.add_argument("-e", "--event", type=int, default=0, help="ID of the event to be displayed")
    parser.add_argument("-d", "--dir", type=str, default=None, help="Directory to save the plot")
    parser.add_argument("-o", "--output", type=str, default=None, help="File name of the output plot")
    parser.add_argument("-s", "--show", type=int, default=1, choices=[0, 1], help="Instantly display or not")
    args = parser.parse_args()

    filename = args.file
    tree = args.tree
    title = args.title
    event_index = args.event
    save_dir = args.dir
    output = args.output
    show = args.show

    plot(filename, tree, event_index, title)

    if save_dir and output:
        plt.savefig(join(save_dir, output))
        print("Figure", join(save_dir, output), "successfully created!")

    if show:
        plt.show()
