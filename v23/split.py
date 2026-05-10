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
from functools import partial

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

def fitfunc(theta, A,b,l):
    theta = theta 
    # theta = np.arccos(1/2*np.cos(alpha)-1/2)
    # phi = np.arcsin(1/np.sqrt(2)*np.sin(alpha))
    return A*np.abs(legendre(l)(np.cos(theta)))+b

def fit_legendre(theta, A, l):
    popt, pcov = curve_fit(partial(fitfunc, l=l), theta, A)
    return popt, pcov

def try_orders(theta, A, n):
    error = 1e3
    order_l = 0
    order_m = 0 
    for i in np.arange(0,(n+1)):
        _, pcov = fit_legendre(theta, A, i)
        error_new = np.sum(np.diag(np.sqrt(np.abs(pcov))))
        if error_new < error:
            error = error_new
            # print(i, error)
            order_l = i
    return order_l

alpha_fit = np.linspace(0, 2*np.pi, 1000)

f_peaks, A_peaks, alpha = get_peaks('raw/ringpeak2-3', [2,2.15], prominence=10, distance=100)
alpha = np.deg2rad(alpha)
fig, ax = plt.subplots(subplot_kw={"projection":"polar"})
ax.plot(alpha, A_peaks, "b.", label="Messdaten")

#Fitte Legendrepolynom
# l = try_orders(alpha, A_peaks, 9)
l = 0
popt, pcov = fit_legendre(alpha, A_peaks, l)
print(popt)
ax.plot(alpha_fit, fitfunc(alpha_fit, *popt, l=l), "r--", label=rf"$Y_{l}^{0}$")
ax.legend()
fig.savefig(dir + "ringpeak2-3_l=0.pdf")

f_peaks, A_peaks, alpha = get_peaks('raw/ringpeak2-3', [2.25,2.27], prominence=0, distance=100)
alpha = np.deg2rad(alpha)
fig, ax = plt.subplots(subplot_kw={"projection":"polar"})
ax.plot(alpha, A_peaks, "b.", label="Messdaten")

#Fitte Legendrepolynom
best_order = try_orders(alpha, A_peaks, 9)
popt, pcov = fit_legendre(alpha, A_peaks, best_order)
print(popt)
ax.plot(alpha_fit, fitfunc(alpha_fit, *popt, l=best_order), "r--", label=rf"$Y_{best_order}^{0}$")
ax.legend()
fig.savefig(dir+ "ringpeak2-3_l=1.pdf")