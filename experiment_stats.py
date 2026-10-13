import numpy as np
import config as cfg 


from functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_barlet_values,
                       score_phi)


def single_error(est):
    return np.abs(cfg.target_phi - est)

def single_est(sigma_noise, M, R) -> float:
    """Считает ошибку для одного эсперемента"""
    
    tau_array = get_tau_array(M, R, cfg.target_phi)
    channel_matrix = get_channel_matrix(t = cfg.t, f = cfg.f, phi_0 = cfg.target_phi, tau_array = tau_array, noise_level = sigma_noise, A = cfg.A, M = M, N = cfg.N)
    W = get_covariation_matrix(channel_matrix, cfg. N)
    E_barlett = get_barlet_values(cfg.phi_vector, M, W)
    est = score_phi(cfg.phi_vector, E_barlett)

    return est

def calculate_mae(sigma_noise: float, K: int, M, R) -> float:
    """Считает среднюю ошибку по множеству равлизаций"""
    return sum([single_error(single_est(sigma_noise, M,R)) for _ in range(K)])/K

def mae_vs_snr(sigma_values, K, M, R):
    """Знеачне ощибки при изменении значения C/Ш"""
    return [calculate_mae(sigma, K, M, R) for sigma in sigma_values]

def mae_vs_sensor_count(sigma, K, M_values, R):
    """Значенеи ошибки при изменении r """
    return [calculate_mae(sigma, K, M, R) for M in M_values]

def mae_vs_radius(sigma, K, M, R_values):
    """Значение ошибки при изменении радиуса решетки"""
    return [calculate_mae(sigma, K, M, R) for R in R_values]









