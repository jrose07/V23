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
        L_new = int((datapath).split('mm')[0].split('vorbereitung_')[1])#mm
        peaks, _ = find_peaks(A, prominence=3, distance=330/(np.pi*2)*np.sqrt((np.pi/L_new)**2 +2e-1), width=[1.5,30], height=7)
        ax.plot(f[peaks], A[peaks], "rx")
        fig.savefig(dir + name)

# #Plotte 75mm Zylinder
plot("raw/vorbereitung_75mm/1_vorbereitung75mm.dat", "1spektrum_75mm.pdf")
plot("raw/vorbereitung_75mm/1_vorbereitung300mm.dat", "1spektrum_300mm.pdf")
plot("raw/vorbereitung_75mm/1_vorbereitung600mm.dat", "1spektrum_600mm.pdf")
# plot("raw/vorbereitung_75mm/1_vorbereitung600mm.dat", "1spektrum_601mm.pdf")

#Get Peaks and do schallgeschwindigkeit with that
# f = omega / 2pi = v/2pi * np.sqrt((Z_mn/r)**2 + (pi * l/L)**2) -> 
def get_peaks(folder):
        L = np.array([])
        df_mean = []
        df_stds = []
        for file in os.scandir(folder):
                if file.is_file():
                        L_new = int((file.name).split('mm')[0].split('vorbereitung')[1]) #mm
                        f, A = np.genfromtxt(file, unpack=True)
                        peaks, _ = find_peaks(A, prominence=3, distance=330/(np.pi*2)*np.sqrt((np.pi/L_new)**2 +2e-1), width=[1.5,30], height=7)
                        f_peaks = f[peaks]
                        df_peaks = np.diff(f_peaks)*1e-3 #kHz
                        df_new = ufloat(np.mean(df_peaks), np.std(df_peaks))
                        df_mean.append(noms(df_new))
                        df_stds.append(stds(df_new))
                        L = np.append(L, L_new)
                        # fig, ax = plt.subplots()
                        # ax.plot(f,A)
                        # ax.plot(f[peaks], A[peaks], "x")
                        # ax.set_title(file.name)
                        # plt.show()
        df = unp.uarray(df_mean, df_stds)
        return L, df

def lineare_regression(folder):
        L, df = get_peaks(folder)
        #Lineare Regression von df gegen L 
        # Plotte df**2 gegen 1/(L**2) und Steigung m = (v_schall/2)**2
        x = 1/L**2
        y = df**2
        fig, ax = plt.subplots()
        ax.errorbar(noms(x), noms(y), yerr=stds(y), color ="blue", linestyle="None", label="Messdaten")

        result = linregress(noms(x), noms(y))
        m = ufloat(result.slope, result.stderr)
        b = ufloat(result.intercept, result.intercept_stderr)
        x_fit = np.linspace(np.min(x), np.max(x),1000)
        ax.plot(x_fit, noms(m)*x_fit+noms(b), "r--", label="Lineare Regression")
        ax.grid()
        ax.legend()
        ax.set(
                xlabel=r"$L^{-2} \, (\mathrm{mm}^{-2})$",
                ylabel=r"$(\Delta f)^2 \, (kHz^2)$"
        )
        ax.ticklabel_format(scilimits=[-4,6])
        fig.savefig(dir + (folder).split('raw/')[1] + ".pdf")
        
        v = unp.sqrt(m)*2
        return v, m, b, L, df

v,m,b,L,df=lineare_regression('raw/vorbereitung_75mm')
add(f"Vorbereitung 75mm:\nFit-Parameter:m={m:.2f}\nb={b:.4f}\nund damit v={v:.2f}m/s\n\n")

# Abweichung vom Theoriewert
v_exp = ufloat(327.5,0.3)
v_theo = 344
dv = np.abs(v_theo-v_exp)/v_theo
add(f"Abweichung vom Theoriewert v_theo = 344m/s ist dv={dv*1e2:.2f} %\n")
#Unterschiede zwischen beiden Geschwindigkeiten
add(f"Abweichung zueinander dv12 = {ufloat(326.39,0.22)-ufloat(328.73,0.65):.2f}\n\n")