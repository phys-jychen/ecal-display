import uproot as up
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D

CrystalLength = 52.5
CrystalWidth = 2.5
CrystalThick = 2.5
nLayer = 18
Bias = 0.5 * CrystalLength

filename = '/lustre/collider/chenjiyuan/ecal-pid/build/test/e-_1GeV.root'

with up.open(filename) as f:
    tree = f['dp']

    event_index = 1

    Hit_X = tree['Hit_X'].array(library='np')
    Hit_Y = tree['Hit_Y'].array(library='np')
    Hit_Z = tree['Hit_Z'].array(library='np') / CrystalThick
    Hit_Energy = tree['Hit_Energy'].array(library='np')

    x = Hit_X[event_index]
    y = Hit_Y[event_index]
    z = np.round(Hit_Z[event_index]).astype(int)
    energy = Hit_Energy[event_index]
    energy_norm = energy / energy.max()

    nentries = len(x)

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    cmap = cm.OrRd

    for i in np.arange(nentries):
        if z[i] % 2 == 0:
            xnew = np.arange(x[i] - Bias, x[i] + 2 * CrystalLength - Bias, CrystalLength)
            ynew = np.arange(y[i], y[i] + 2 * CrystalWidth, CrystalWidth)
        else:
            xnew = np.arange(x[i], x[i] + 2 * CrystalWidth, CrystalWidth)
            ynew = np.arange(y[i] - Bias, y[i] + 2 * CrystalLength - Bias, CrystalLength)

        xnew, ynew = np.meshgrid(xnew, ynew)
        znew = z[i] * np.ones((2, 2))
        enew = energy_norm[i] * np.ones((2, 2))

        ax.plot_surface(xnew, znew, ynew, cmap=cmap, facecolors=cmap(enew), edgecolor='k', alpha=0.75, lw=0.2, rstride=1, cstride=1, antialiased=False)
#        surf = ax.plot_surface(xnew, znew, ynew, cmap='coolwarm', alpha=0.8, lw=0.1, rstride=1, cstride=1, antialiased=False)

    ax.set_xticks(np.arange(-30, 31, 10))
    ax.set_ylim(0, 24)
    ax.set_yticks(np.arange(0, nLayer + 1, 3))
    ax.set_zticks(np.arange(-30, 31, 10))

    fig.suptitle(r"1-GeV $e^-$", size='xx-large')
    ax.invert_xaxis()
    ax.set_xlabel("X [cm]")
    ax.set_ylabel("Z [layer]")
    ax.set_zlabel("Y [cm]")

    m = plt.cm.ScalarMappable(cmap=cmap)
    m.set_array(energy)
    plt.colorbar(m, pad=0.2, label="Hit Energy [MeV]")
#    fig.colorbar(surf, pad=0.2, label="Hit Energy [MeV]")

    ax.view_init(elev=25, azim=-40, roll=0)

    plt.savefig('figs/EventDisplay_e-_1GeV_energy.pdf')
    print("figs/EventDisplay_e-_1GeV_energy.pdf successfully created!")
    plt.show()
