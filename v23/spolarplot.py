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
from scipy.special import legendre
from scipy.special import sph_harm_y
from functools import partial

dir = "content/plots/"
dir_tab = "content/tables/"

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
    alpha = np.array([])
    for file in os.scandir(folder):
        if file.is_file():
            f_peaks = np.append(f_peaks, get_peaks(file, *args, **kwargs)[0])
            A_peaks = np.append(A_peaks, get_peaks(file, *args, **kwargs)[1])
            alpha = np.append(alpha, int((file.name).split('.', 1)[0]))
    return f_peaks, A_peaks, alpha

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

def get_sharm(alpha, l, m):
    """ Input alpha has to be in radians"""
    theta = np.arccos(-1/2*(1-np.cos(alpha)))
    # phi = np.arctan(-1/(2*np.sqrt(2))*(1-np.cos(alpha))/np.sin(alpha))
    phi = np.arcsin(1/np.sqrt(2)*np.sin(alpha))
    return np.real(sph_harm_y(l,m,theta,phi))

def fitfunc(alpha, A, b, l, m):
    alpha = alpha 
    theta = np.arccos(1/2*(np.cos(alpha)-1))
    phi = np.atan2(1/np.sqrt(2)*np.sin(alpha), 1/2*(1-np.cos(alpha)))
    return A*np.abs(np.real(sph_harm_y(l,m,theta,phi))) + b

def fit_sharm(alpha, A, l, m):
    popt, pcov = curve_fit(partial(fitfunc, l=l, m=m), alpha, A)
    return popt, pcov

# subplot_kw={"projection":"polar"}

def try_orders(alpha, A, n):
    error = 1e3
    order_l = 0
    order_m = 0 
    for i in np.arange(0,(n+1)):
        for j in range(i):
            popt, pcov = fit_sharm(alpha, A, i, j)
            error_new = np.sum(np.diag(np.sqrt(np.abs(pcov))))
            if error_new < error:
                error = error_new
                # print(i, error)
                order_l = i
                order_m = j
    return order_l, order_m

def spolarplot(folder, name, l, m, *args, **kwargs):
    f_peaks, A_peaks, alpha= accumulate_peaks(folder, *args, **kwargs)
    alpha = np.deg2rad(alpha)
    fig, ax = plt.subplots(subplot_kw={"projection":"polar"})
    #Normalize A_peaks to Maximum of A_peaks:
    A_exp = A_peaks
    ax.plot(alpha, A_exp, ".", label="Experimentelle Daten")
    
    alpha_fit = np.linspace(0, 2*np.pi, 1000)
    
    #Fit A_sharm with right amplitude to A_exp
    bl, bm = try_orders(alpha, A_exp, 9)
    bl = l
    bm = m
    # print("Best Order: ", bl, bm)
    popt, pcov = fit_sharm(alpha, A_exp, bl,bm)
    perr = np.diag(np.sqrt(np.abs(pcov)))
    # print(name, popt, perr, np.linalg.cond(pcov))
    ax.plot(alpha_fit, fitfunc(alpha_fit, *popt, l=bl, m=bm), "r--", label=rf"$Y_{bl}^{bm}$")
    # ax.plot(alpha_fit, fitfunc(alpha_fit, *popt, l=l, m=m), "g--", label=f"Theoriefit mit eigenem l,m = {l}, {m}")
    
    ax.set(
        xlabel=r"$\alpha \, (\circ)$",
        ylabel=r"$A \, (a.u.)$"
    )
    ax.legend(loc='lower center')
    fig.savefig(dir + name)

spolarplot("raw/peak2-3", "peak2-3.pdf",1, 0)
spolarplot("raw/peak3-7", "peak3-7.pdf",2, 0)
spolarplot("raw/peak4-9", "peak4-9.pdf",3, 0)
spolarplot("raw/peak7-4", "peak7-4.pdf",5, 0)

# PLot Übersicht über alle Peaks für 180 Grad
f, A = np.genfromtxt('raw/3_uerbesicht180grad.dat', unpack=True)
fig, ax = plt.subplots()
ax.plot(f*1e-3,A)
ax.grid()
ax.set(
    xlabel=r"$f \, (kHz)$",
    ylabel=r"$A \, (a.u.)$"
)
fig.savefig(dir + 'Übersicht180Grad.pdf')