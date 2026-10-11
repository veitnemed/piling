import numpy as np
import matplotlib.pyplot as plt
import config as cfg 
from config import (SENSOR_COUNTS, SNR_VALUES, FIX_SIGMA, REALESATION_COUNT, STANDART_DIVIATONS_NOISE)
import time

from functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_barlet_values,
                       score_phi)


def single_error(sigma_noise, M) -> float:
    """Считает ошибку для одного эсперемента"""
    
    tau_array = get_tau_array(M, cfg.R, cfg.target_phi)
    channel_matrix = get_channel_matrix(t = cfg.t, f = cfg.f, phi_0 = cfg.target_phi, tau_array = tau_array, noise_level = sigma_noise, A = cfg.A, M = M, N = cfg.N)
    W = get_covariation_matrix(channel_matrix, cfg. N)
    E_barlett = get_barlet_values(cfg.phi_vector, M, W)
    est = score_phi(cfg.phi_vector, E_barlett)
    delta = np.abs(cfg.target_phi - est)
    return delta

def calculate_mae(sigma_noise: float, K: int,M) -> float:
    """Считает среднюю ошибку по множеству равлизаций"""
    return sum([single_error(sigma_noise, M) for _ in range(K)])/K

def mae_vs_snr(sigma_values, K, M):
    """Знеачне ощибки при изменении значения C/Ш"""
    return [calculate_mae(sigma, K, M) for sigma in sigma_values]

def mae_vs_sensor_count(sigma, K, M_values):
    """Значенеи ошибки при изменении r """
    return [calculate_mae(sigma, K, M) for M in M_values]

start_time = time.perf_counter()
snr_maes = mae_vs_snr(STANDART_DIVIATONS_NOISE, REALESATION_COUNT, cfg.M)
sensor_maes = mae_vs_sensor_count(FIX_SIGMA, REALESATION_COUNT, SENSOR_COUNTS)
end_time = time.perf_counter()
delta_time = end_time - start_time
print(f"Время рассчёта {round(delta_time,2)} сек.")

plt.plot(SNR_VALUES, snr_maes)
plt.title("Зависимость " + r"$\varepsilon$" + " от SNR ")
plt.ylabel("Ошибка оценки (МАЕ) " + r"$\varepsilon$" + ", рад.")
plt.xlabel("Отношение сигнал/шум  M, шт")
plt.grid(True)
plt.show()

plt.plot(SENSOR_COUNTS, sensor_maes)
plt.title("Зависимость " + r"$\varepsilon$" + " от M  (Кол-во датчиков) ")
plt.ylabel("Ошибка оценки (МАЕ) " + r"$\varepsilon$" + ", рад.")
plt.xlabel("Колчиество датчиков M, шт")
plt.grid(True)
plt.show()





