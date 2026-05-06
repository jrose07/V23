import uncertainties.unumpy as unp
import numpy as np
from scipy.optimize import curve_fit
from addons import write, add, latex_float, tab_to_latex as tab2tex
from scipy.stats import linregress
from uncertainties import ufloat
from uncertainties.unumpy import nominal_values as noms, std_devs as stds
import scipy.constants as const
import matplotlib.pyplot as plt

dir = "content/plots/"
dir_tab = "content/tables/"

def plot(datapath, name):
        f, A = np.genfromtxt(datapath, unpack=True)
        f*=1e-3 #from Hz to kHz
        fig, ax = plt.subplots()
        ax.plot(f, A)
        ax.grid()
        ax.set(
                xlabel=r"$f \, (\mathrm{kHz})$",
                ylabel=r"Amplitude $\,$ (a.u.)"
        )
        fig.savefig(dir + name)

#Plotte 50mm Zylinder
plot("raw/vorbereitung_50mm/2_vorbereitung50mm.dat", "2spektrum_50mm.pdf") 
plot("raw/vorbereitung_50mm/2_vorbereitung200mm.dat", "2spektrum_200mm.pdf")
plot("raw/vorbereitung_50mm/2_vorbereitung400mm.dat", "2spektrum_400mm.pdf")
plot("raw/vorbereitung_50mm/2_vorbereitung600mm.dat", "2spektrum_600mm.pdf")
#Plotte 75mm Zylinder
plot("raw/vorbereitung_75mm/1_vorbereitung75mm.dat", "1spektrum_75mm.pdf")
plot("raw/vorbereitung_75mm/1_vorbereitung300mm.dat", "1spektrum_300mm.pdf")
plot("raw/vorbereitung_75mm/1_vorbereitung600mm.dat", "1spektrum_600mm.pdf")
plot("raw/vorbereitung_75mm/1_vorbereitung600mm.dat", "1spektrum_601mm.pdf")