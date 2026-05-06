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

    # fig, ax = plt.subplots()
    # ax.plot(f, A, label="Data")
    # ax.plot(f[peaks], A[peaks] , "x")
    # plt.show()

def get_peaks(datapath, *args, **kwargs):
    f, A = np.genfromtxt(datapath, unpack=True)
    peaks, _ = find_peaks(A, *args, **kwargs)
    A_peak = np.max(A[peaks])
    index = np.where(np.isclose(A, A_peak))
    # print(index, f[index], A[index], A_peak, A[peaks])
    return f[index], A[index]

def accumulate_peaks(folder, *args, **kwargs):
    f_peaks = np.array([])
    A_peaks = np.array([])
    phi = np.array([])
    for file in os.scandir(folder):
        if file.is_file():
            f_peaks = np.append(f_peaks, get_peaks(file, *args, **kwargs)[0])
            A_peaks = np.append(A_peaks, get_peaks(file, *args, **kwargs)[1])
            phi = np.append(phi, int((file.name).split('.', 1)[0]))
    return f_peaks, A_peaks, phi

def polarplot(folder, name, *args, **kwargs):
    f_peaks, A_peaks, phi= accumulate_peaks(folder, *args, **kwargs)
    phi = np.deg2rad(phi)
    fig, ax = plt.subplots(subplot_kw={'projection':'polar'})
    ax.plot(phi, A_peaks, ".")
    fig.savefig("v23/" + dir + name)

def plot_peaks(folder, *args, **kwargs):
    i = 0
    for file in os.scandir(folder):
        if file.is_file():
            f, A = np.genfromtxt(file, unpack=True)
            fig, ax = plt.subplots()
            ax.plot(f, A)
            f_peaks, A_peaks = get_peaks(file, *args, **kwargs)
            ax.plot(f_peaks, A_peaks, "x")
            ax.grid()
            plt.show()
            print(i, file.name)
            i+=1

# get_peaks("v23/raw/peak4-9/0.dat", prominence=10)
polarplot("v23/raw/peak2-3", "peak2-3.pdf", prominence=0)
polarplot("v23/raw/peak3-7", "peak3-7.pdf", prominence=0)
polarplot("v23/raw/peak4-9", "peak4-9.pdf", prominence=0)
polarplot("v23/raw/peak7-4", "peak7-4.pdf", prominence=0)

# plot_peaks("v23/raw/peak4-9")