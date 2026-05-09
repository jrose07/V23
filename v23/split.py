import uncertainties.unumpy as unp
import numpy as np
from scipy.optimize import curve_fit
from addons import write, add, latex_float, tab_to_latex as tab2tex
from scipy.stats import linregress
from uncertainties import ufloat
from uncertainties.unumpy import nominal_values as noms, std_devs as stds
import scipy.constants as const
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os

dir = "content/plots/"
dir_tab = "content/tables/"

#Plotte 3 Peaks für Ringe
fig, ax = plt.subplots()
f,A = np.genfromtxt('raw/4_3mmring.dat', unpack=True)
f*=1e-3 # kHz
ax.plot(f,A)
ax.grid()
ax.set(
    xlabel=r"$f \, (kHz)$",
    ylabel=r"$A \, (a.u.)$"
)
fig.savefig(dir + '3mmring.pdf')
ax.clear()
f,A = np.genfromtxt('raw/4_6mmring.dat', unpack=True)
f*=1e-3 # kHz
ax.plot(f,A)
ax.grid()
ax.set(
    xlabel=r"$f \, (kHz)$",
    ylabel=r"$A \, (a.u.)$"
)
fig.savefig(dir + '6mmring.pdf')
ax.clear()
f,A = np.genfromtxt('raw/4_9mmring.dat', unpack=True)
f*=1e-3 # kHz
ax.plot(f,A)
ax.grid()
ax.set(
    xlabel=r"$f \, (kHz)$",
    ylabel=r"$A \, (a.u.)$"
)
fig.savefig(dir + '9mmring.pdf')
plt.close(fig)


#Plotte Polarplot für 9mmRing-Peaks
# def get_peaks(datapath, *args, **kwargs):
#     f, A = np.genfromtxt(datapath, unpack=True)
#     peaks, _ = find_peaks(A, *args, **kwargs)
#     A_peak = np.max(A[peaks])
#     index = np.where(np.isclose(A, A_peak))
#     # print(index, f[index], A[index], A_peak, A[peaks])
#     return f[index], A[index]

def get_peaks(folder, range, *args, **kwargs):
    f_peaks = np.array([])
    A_peaks = np.array([])
    alpha = np.array([])
    for file in os.scandir(folder):
        if file.is_file():
            f, A = np.genfromtxt(file, unpack=True)
            f*=1e-3 #kHz
            mask = (f >= range[0]) & (f <= range[1])
            f = f[mask]
            A = A[mask]
            peaks, _ = find_peaks(A, *args, **kwargs)
            f_peaks = np.append(f_peaks, f[peaks])
            A_peaks = np.append(A_peaks, A[peaks])
            alpha = np.append(alpha, int((file.name).split('.', 1)[0]))
            # fig, ax = plt.subplots()
            # ax.plot(f, A)
            # ax.plot(f[peaks], A[peaks], "x")
            # ax.grid()
            # ax.set_title(file.name)
            # plt.show()
    return f_peaks, A_peaks, alpha

f_peaks, A_peaks, alpha = get_peaks('raw/ringpeak2-3', [2,2.15], prominence=10, distance=100)
alpha = np.deg2rad(alpha)
fig, ax = plt.subplots(subplot_kw={"projection":"polar"})
ax.plot(alpha, A_peaks, "b.")
fig.savefig(dir + "ringpeak2-3_l=0.pdf")

f_peaks, A_peaks, alpha = get_peaks('raw/ringpeak2-3', [2.25,2.27], prominence=0, distance=100)
# print(np.mean(f_peaks))
alpha = np.deg2rad(alpha)
fig, ax = plt.subplots(subplot_kw={"projection":"polar"})
ax.plot(alpha, A_peaks, "b.")
fig.savefig(dir+ "ringpeak2-3_l=1.pdf")