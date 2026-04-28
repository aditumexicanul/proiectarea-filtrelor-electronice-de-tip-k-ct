import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

def Filtru_trece_jos():
    print('Proiectare filtru trece-jos k constant de tip T (o singura sectiune)')

    fc = float(input('Introdu frecventa de taiere fc [Hz]: '))        # frecventa de taiere
    R0 = float(input('Introdu impedanta caracteristica R [ohmi]: '))  # impedanta caracteristica de proiectare

    L1 = R0 / (np.pi * fc)
    C2 = 1 / (np.pi * fc * R0)

    print(f'\nRezultate:')
    print(f'L1 = {L1:.6e} H')
    print(f'C2 = {C2:.6e} F')
    print(f'---------------------')
    print(f'L1 = {L1*1e3:.6f} mH')
    print(f'C2 = {C2*1e6:.6f} uF')

    f = np.logspace(1, 6, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Z1 = 1j * w * (L1 / 2)          # fiecare inductanta serie
    Z2 = 1 / (1j * w * C2)          # condensatorul transversal

    Z_right = Z1 + RL               # ramura dreapta vazuta din nodul central
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)   # paralel intre C si ramura dreapta
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL              # tensiunea pe sarcina

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    ct=1
    fc1=0
    fc2=0

    grafic(f, A_dB, fc, fc1, fc2, ct)
    pass

def Filtru_trece_sus():
    print('Proiectare filtru trece-sus k constant de tip T (o singura sectiune)')

    fc = float(input('Introdu frecventa de taiere fc [Hz]: '))        # frecventa de taiere
    R0 = float(input('Introdu impedanta caracteristica R [ohmi]: '))  # impedanta caracteristica de proiectare

    C1 = 1 / (4 * np.pi * R0 * fc)
    L2 = R0 / (4 * np.pi * fc)

    print(f'\nRezultate:')
    print(f'C1 = {C1:.6e} F')
    print(f'L2 = {L2:.6e} H')
    print(f'---------------------')
    print(f'C1 = {C1*1e6:.6f} uF')
    print(f'L2 = {L2*1e3:.6f} mH')

    f = np.logspace(1, 6, 2000)
    w = 2 * np.pi * f
    Vin = 1.0
          
    Z1 = 1 / (1j * w * 2 * C1)
    Z2 = 1j * w * L2

    Z_right = Z1 + RL               # ramura dreapta vazuta din nodul central
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)   # paralel intre C si ramura dreapta
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL              # tensiunea pe sarcina

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    ct=2
    fc1=0
    fc2=0

    grafic(f, A_dB, fc, fc1, fc2, ct)
    pass

def Filtru_trece_banda():
    print('Proiectare filtru trece-banda k constant de tip T (o singura sectiune)')

    fc1 = float(input('Introdu frecventa de taiere inferioara fc1 [Hz]: '))        # frecventa de taiere
    fc2 = float(input('Introdu frecventa de taiere superioara fc2 [Hz]: '))        # frecventa de taiere
    R0 = float(input('Introdu impedanta caracteristica R [ohmi]: '))  # impedanta caracteristica de proiectare
    dF = fc2 - fc1 # delta frecventelor de taiere
    pF = fc1 * fc2 # produsul frecventelor de taiere

    L1 = R0 / (np.pi * dF)
    C1 = dF / (4 * np.pi * R0 * pF)
    L2 = (R0 * dF) / (4 * np.pi * pF)
    C2 = 1 / (np.pi * R0 * dF)

    print(f'\nRezultate:')
    print(f'L1 = {L1:.6e} F')
    print(f'C1 = {C1:.6e} H')
    print(f'L2 = {L2:.6e} F')
    print(f'C2 = {C2:.6e} H')
    print(f'---------------------')
    print(f'L1 = {L1*1e3:.6f} mH')
    print(f'C1 = {C1*1e6:.6f} uF')
    print(f'L2 = {L2*1e3:.6f} mH')
    print(f'C2 = {C2*1e6:.6f} uF')

    f = np.logspace(1, 7, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Zl1 = 1j * w * (L1 / 2)
    Zc1 = 1 / (1j * w * 2 * C1)
    Zl2 = 1j * w * L2
    Zc2 = 1 / (1j * w * C2)   

    Z1 = Zl1 + Zc1
    Z2 = (Zl2 * Zc2)/(Zl2 + Zc2)

    Z_right = Z1 + RL               # ramura dreapta vazuta din nodul central
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)   # paralel intre C si ramura dreapta
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL              # tensiunea pe sarcina

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    ct=3
    fc=0

    grafic(f, A_dB, fc, fc1, fc2, ct)
    pass

def Filtru_opreste_banda():
    print('Proiectare filtru opreste-banda k constant de tip T (o singura sectiune)')

    fc1 = float(input('Introdu frecventa de taiere inferioara fc1 [Hz]: '))        # frecventa de taiere
    fc2 = float(input('Introdu frecventa de taiere superioara fc2 [Hz]: '))        # frecventa de taiere
    R0 = float(input('Introdu impedanta caracteristica R [ohmi]: '))  # impedanta caracteristica de proiectare
    dF = fc2 - fc1 # delta frecventelor de taiere
    pF = fc1 * fc2 # produsul frecventelor de taiere

    L1 = (R0 * dF) / (np.pi * pF)
    C1 = 1 / (4 * np.pi * R0 * dF)
    L2 = R0 / (4 * np.pi * dF)
    C2 = dF / (np.pi * R0 * pF)

    print(f'\nRezultate:')
    print(f'L1 = {L1:.6e} F')
    print(f'C1 = {C1:.6e} H')
    print(f'L2 = {L2:.6e} F')
    print(f'C2 = {C2:.6e} H')
    print(f'---------------------')
    print(f'L1 = {L1*1e3:.6f} mH')
    print(f'C1 = {C1*1e6:.6f} uF')
    print(f'L2 = {L2*1e3:.6f} mH')
    print(f'C2 = {C2*1e6:.6f} uF')

    f = np.logspace(1, 7, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Zl1 = 1j * w * (L1 / 2)
    Zc1 = 1 / (1j * w * 2 * C1)
    Zl2 = 1j * w * L2
    Zc2 = 1 / (1j * w * C2)   

    Z1 = (Zl1 * Zc1)/(Zl1 + Zc1)
    Z2 = Zl2 + Zc2

    Z_right = Z1 + RL               # ramura dreapta vazuta din nodul central
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)   # paralel intre C si ramura dreapta
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL              # tensiunea pe sarcina

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    ct=4
    fc=0

    grafic(f, A_dB, fc, fc1, fc2, ct)
    pass

def grafic(f, A_dB, fc, fc1, fc2, ct):
    plt.figure(figsize=(10, 6))
    plt.semilogx(f, A_dB, label='|Vout/Vin| [dB]')

    if ct == 1:
        plt.axvline(fc, color='red', linestyle='--', label=f'fc = {fc:.0f} Hz')
        plt.title('Caracteristica de amplitudine a filtrului trece-jos k constant, sectiune T')
    elif ct == 2:
        plt.axvline(fc, color='red', linestyle='--', label=f'fc = {fc:.0f} Hz')
        plt.title('Caracteristica de amplitudine a filtrului trece-sus k constant, sectiune T')
    elif ct == 3:
        plt.axvline(fc1, color='red', linestyle='--', label=f'fc1 = {fc1:.0f} Hz')
        plt.axvline(fc2, color='red', linestyle='--', label=f'fc2 = {fc2:.0f} Hz')
        plt.title('Caracteristica de amplitudine a filtrului trece-banda k constant, sectiune T')
    elif ct == 4:
        plt.axvline(fc1, color='red', linestyle='--', label=f'fc1 = {fc1:.0f} Hz')
        plt.axvline(fc2, color='red', linestyle='--', label=f'fc2 = {fc2:.0f} Hz')
        plt.title('Caracteristica de amplitudine a filtrului opreste-banda k constant, sectiune T')
    
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.xlabel('Frecventa [Hz]')
    plt.ylabel('Amplitudine [dB]')
    plt.legend()
    plt.tight_layout()
    plt.show()


Rs = 50           # rezistenta sursei
RL = 50           # rezistenta de sarcina

print('Ce filtru doriti sa proiectati?')
print('FTJ - 1\nFTS - 2\nFTB - 3\nFOB - 4')
rasp = int(input('Raspuns: '))

if rasp == 1:
    Filtru_trece_jos()
elif rasp == 2:
    Filtru_trece_sus()
elif rasp == 3:
    Filtru_trece_banda()
elif rasp == 4:
    Filtru_opreste_banda()
else:
    pass