import numpy as np

fs = 8800 # ЧАСТОТА ДИСКРЕТИЗАЦИИ
dt = 1/fs # ШАГ ДИСКРЕТИЗАЦИИ
N = 10000 # КОЛИЧЕСТВО ТОЧЕК 
t = np.arange(N)*dt #ВЕКТОР ВРЕМЕНИ

delta_phi = 0.001 # Шаг поиска угла 0.0003
N_phi = int(2*np.pi/delta_phi) # Количество значений угла 
phi_vector = np.linspace(0,2*np.pi,N_phi) # Значения угла от 0 до 2П

# ПАРАМЕТРЫ АВП
M = 5 # КОЛИЧЕСТВО ДАТЧИКОВ

c = 343.26 # СКОРОСТЬ ЗВУКА


# ПАРАМЕТРЫ СИГНАЛА 
f = 10 # ЦЕНТРАЛЬНАЯ ЧАСТОТА СИГНАЛА 
A = 1 # АМПЛИТУДА СИГНАЛА 
alpha = 10
R = c/(2*f*alpha)
target_phi = np.pi/2 # АЗИМУТ ПОД КОТОРЫМ ПРИХОДИТ ИСГНАЛ (ТО ЧТО ОЦЕНИВАЕМ)


# Параметры шумы
sigma_noise = 0.5
REALESATION_COUNT = 50
SNR_VALUES = np.array(list(range(1,11)))
STANDART_DIVIATONS_NOISE = A / np.sqrt(SNR_VALUES)

SENSOR_COUNTS = [1, 2, 3, 4, 5, 7, 10]
ALPHA_VALUES_1 = np.array(list(range(10,20)))
ALPHA_VALUES_2 = np.array(list(range(10,100,10)))

R_min = 0.1
R_max = 10.0
R_VALUES = np.linspace(R_min, R_max, 10)

FIX_SIGMA = 0.3
TIME_LIMIT = {"left": 0,
        "right": 0.15}

PHI_VALUES = np.linspace(0,2*np.pi,36)