# import uncertainties.unumpy as unp
# import numpy as np
# from scipy.optimize import curve_fit
# from addons import write, add, latex_float, tab_to_latex as tab2tex
# from scipy.stats import linregress
# from uncertainties import ufloat
# from uncertainties.unumpy import nominal_values as noms, std_devs as stds
# import scipy.constants as const
# import matplotlib.pyplot as plt
# from scipy.signal import find_peaks
# import os
# from scipy.special import legendre
# from scipy.special import sph_harm_y

# dir = "content/plots/"
# dir_tab = "content/tables/"

# def get_peaks(datapath, *args, **kwargs):
#     f, A = np.genfromtxt(datapath, unpack=True)
#     peaks, _ = find_peaks(A, *args, **kwargs)
#     A_peak = np.max(A[peaks])
#     index = np.where(np.isclose(A, A_peak))
#     # print(index, f[index], A[index], A_peak, A[peaks])
#     return f[index], A[index]

# def accumulate_peaks(folder, *args, **kwargs):
#     f_peaks = np.array([])
#     A_peaks = np.array([])
#     alpha = np.array([])
#     for file in os.scandir(folder):
#         if file.is_file():
#             f_peaks = np.append(f_peaks, get_peaks(file, *args, **kwargs)[0])
#             A_peaks = np.append(A_peaks, get_peaks(file, *args, **kwargs)[1])
#             alpha = np.append(alpha, int((file.name).split('.', 1)[0]))
#     return f_peaks, A_peaks, alpha

# def fitfunc0(x,Amp, b):
#     polynom = legendre(0)
#     return Amp*polynom(x) + b

# def fitfunc1(x,Amp, b):
#     polynom = legendre(1)
#     return Amp*polynom(x) + b

# def fitfunc2(x,Amp, b):
#     polynom = legendre(2)
#     return Amp*polynom(x) + b

# def fitfunc3(x,Amp, b):
#     polynom = legendre(3)
#     return Amp*polynom(x) + b

# def fitfunc4(x,Amp, b):
#     polynom = legendre(4)
#     return Amp*polynom(x) + b

# def fitfunc5(x,Amp, b):
#     polynom = legendre(5)
#     return Amp*polynom(x) + b

# def fitfunc6(x,Amp, b):
#     polynom = legendre(6)
#     return Amp*polynom(x) + b

# def fitfunc7(x,Amp, b):
#     polynom = legendre(7)
#     return Amp*polynom(x) + b

# def fitfunc8(x,Amp, b):
#     polynom = legendre(8)
#     return Amp*polynom(x) + b

# def fitfunc9(x,Amp, b):
#     polynom = legendre(9)
#     return Amp*polynom(x) + b

# def fit_legendre(theta, A, n, p0):
#     x = np.cos(theta)
#     match n:
#         case 0:
#             f = fitfunc0
#         case 1: 
#             f = fitfunc1
#         case 2:
#             f = fitfunc2
#         case 3:
#             f = fitfunc3
#         case 4:
#             f = fitfunc4
#         case 5:
#             f = fitfunc5
#         case 6:
#             f = fitfunc6
#         case 7:
#             f = fitfunc7
#         case 8:
#             f = fitfunc8
#         case 9:
#             f = fitfunc9
#     pcov, popt = curve_fit(f, x, A, p0=p0)
#     return pcov, popt, f

# def plot_peaks(folder, *args, **kwargs):
#     i = 0
#     for file in os.scandir(folder):
#         if file.is_file():
#             f, A = np.genfromtxt(file, unpack=True)
#             fig, ax = plt.subplots()
#             ax.plot(f, A)
#             f_peaks, A_peaks = get_peaks(file, *args, **kwargs)
#             ax.plot(f_peaks, A_peaks, "x")
#             ax.grid()
#             plt.show()
#             print(i, file.name)
#             i+=1

# def get_sharm(alpha, l, m):
#     """ Input alpha has to be in radians"""
#     theta = np.arccos(-1/2*(1-np.cos(alpha)))
#     # phi = np.arctan(-1/(2*np.sqrt(2))*(1-np.cos(alpha))/np.sin(alpha))
#     phi = np.arcsin(1/np.sqrt(2)*np.sin(alpha))
#     return np.real(sph_harm_y(l,m,theta,phi))

# def fitfunc(x,A,c):
#     return A*(x-c)

# def polarplot(folder, name, n, p0, *args, **kwargs):
#     f_peaks, A_peaks, alpha= accumulate_peaks(folder, *args, **kwargs)
#     alpha = np.deg2rad(alpha)
#     #Convert alpha into Polarangle Theta:
#     theta = np.arccos(-1/2*(1+np.cos(alpha)))
#     fig, ax = plt.subplots(subplot_kw={'projection':'polar'})
#     ax.plot(theta, A_peaks, ".", label="Theta-Abhängigkeit")
    
#     #Fit Legendre-Polynom
#     popt, pcov, fitfunc = fit_legendre(theta, A_peaks, n, p0)
#     perr = np.diag(np.sqrt(popt))
#     print(pcov, perr)
#     theta_fit = np.linspace(0, 2*np.pi, 100)
#     ax.plot(theta_fit, fitfunc(np.cos(theta_fit), *pcov), "r.", label="Theoriefit")
#     ax.legend()
#     fig.savefig( dir + name)

# def fit_spharm(alpha, A, l, m):
#     popt, pcov = curve_fit()
    

# def spolarplot(folder, name, l,m, *args, **kwargs):
#     f_peaks, A_peaks, alpha= accumulate_peaks(folder, *args, **kwargs)
#     alpha = np.deg2rad(alpha)
#     #Cutoff first 6 values
#     fig, ax = plt.subplots()
#     #Normalize A_peaks to Maximum of A_peaks:
#     A_exp = A_peaks/np.max(A_peaks)
#     ax.plot(alpha, A_exp, ".", label="Alpha-Abhängigkeit")
    
#     alpha_fit = np.linspace(0, 2*np.pi, 1000)
#     A_sharm = get_sharm(alpha, l, m)
    
#     #Fit A_sharm with right amplitude to A_exp
#     popt, pcov = curve_fit(fitfunc, A_sharm, A_exp)
#     perr = np.diag(np.sqrt(np.abs(pcov)))
#     # print(np.linalg.cond(pcov))
#     print(name, popt, perr, np.linalg.cond(pcov))
#     # print(get_sharm(1, l, m), fitfunc(get_sharm(1,l,m), *popt))
#     ax.plot(alpha_fit, fitfunc(get_sharm(alpha_fit, l, m), *popt), "r--", label="Theoriefit")
#     # ax.plot(alpha_fit, fitfunc(get_sharm(alpha_fit-, l, m), 0.43, -0.63-np.pi)-1.3, "g--")
#     ax.legend()
#     fig.savefig(dir + name)

# # polarplot("raw/peak2-3", "peak2-3.pdf",1, prominence=0, p0=[20, 0])
# # polarplot("raw/peak3-7", "peak3-7.pdf",3, prominence=0, p0=[10,0])
# # polarplot("raw/peak4-9", "peak4-9.pdf",3, prominence=0, p0=[20,  0])
# # polarplot("raw/peak7-4", "peak7-4.pdf",7, prominence=0, p0=[20, 0])

# spolarplot("raw/peak2-3", "peak2-3.pdf",3, 0)
# spolarplot("raw/peak3-7", "peak3-7.pdf",4, 0)
# spolarplot("raw/peak4-9", "peak4-9.pdf",5, 0)
# spolarplot("raw/peak7-4", "peak7-4.pdf",6, 0)


# # PLot Übersicht über alle Peaks für 180 Grad
# f, A = np.genfromtxt('raw/3_uerbesicht180grad.dat', unpack=True)
# fig, ax = plt.subplots()
# ax.plot(f*1e-3,A)
# ax.grid()
# fig.savefig(dir + 'Übersicht180Grad.pdf')
