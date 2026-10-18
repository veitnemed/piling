import numpy as np


# ПАРАМЕТРЫ МОДЕЛИ 
fs = 8800 # ЧАСТОТА ДИСКРЕТИЗАЦИИ
dt = 1/fs # ШАГ ДИСКРЕТИЗАЦИИ
N = 10000 # КОЛИЧЕСТВО ТОЧЕК 
t = np.arange(N)*dt #ВЕКТОР ВРЕМЕНИ

delta_phi = 0.001 # Шаг поиска угла 0.0003
N_phi = int(2*np.pi/delta_phi) # Количество значений угла 
phi_vector = np.linspace(0,2*np.pi,N_phi,endpoint= False) # Значения угла от 0 до 2П

# ПАРАМЕТРЫ АВП
M = 3 # КОЛИЧЕСТВО ДАТЧИКОВ
c = 343.26 # СКОРОСТЬ ЗВУКА


# ПАРАМЕТРЫ СИГНАЛА 
f = 10 # ЦЕНТРАЛЬНАЯ ЧАСТОТА СИГНАЛА 
A = 1 # АМПЛИТУДА СИГНАЛА 
alpha = 10
R = c / (2*f*alpha)
TARGET_PHI = np.pi/2 # АЗИМУТ ПОД КОТОРЫМ ПРИХОДИТ ИСГНАЛ (ТО ЧТО ОЦЕНИВАЕМ)

f1 = c/(2*R*alpha)
R1 = 1

# Параметры шумы

REALESATION_COUNT = 500

# ПАРАМЕТРЫ ЭКСПЕРИМЕНТА 

SENSOR_VALUES = [1, 2, 3, 4, 5, 7, 10]

SNR_VALUES1 = np.linspace(1, 10, 10)
SNR_VALUES2 = np.linspace(5, 20, 5)
NOISE_LEVEL_VALUES1 = A/np.sqrt(SNR_VALUES1)
NOISE_LEVEL_VALUES2 = A/np.sqrt(SNR_VALUES2)

ALPHA_VALUES_2 = np.arange(0,1, 0.01)
ALPHA_VALUES_1 = np.arange(1,10,1)
R_min = 0.1
R_max = 10.0
R_VALUES = np.linspace(R_min, R_max, 10)


STANDART_DIVIATONS_NOISE = A/np.sqrt(np.array(SNR_VALUES1))

SNR = 2
NOISE_LEVEL = 0.3
TIME_LIMIT = {"left": 0,
        "right": 0.15}

PHI_VALUES = np.linspace(0,2*np.pi,90, endpoint = False)

CONFIG_PARAMETRS = {"snr": SNR,
        "M": M,
        "R": R,
        "f0": f,
        "K": REALESATION_COUNT,
        "target_phi": TARGET_PHI}

