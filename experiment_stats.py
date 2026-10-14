import numpy as np
import config as cfg 


from functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_barlet_values,
                       score_phi)


def single_error(est, target_phi):
    return np.abs((est - target_phi + np.pi) % (2 * np.pi) - np.pi)
def single_est(sigma_noise, M, R, target_phi) -> float:
    tau_array = get_tau_array(M, R, target_phi)
    channel_matrix = get_channel_matrix(t=cfg.t, f=cfg.f, phi_0=target_phi, 
                                       tau_array=tau_array, noise_level=sigma_noise, 
                                       A=cfg.A, M=M, N=cfg.N)
    W = get_covariation_matrix(channel_matrix, cfg.N)
    E_barlett = get_barlet_values(cfg.phi_vector, M, W)
    est = score_phi(cfg.phi_vector, E_barlett)
    return est

def calculate_variance(sigma_noise, K, M, R, target_phi=cfg.target_phi):
    if K < 2:
        raise ValueError("Для расчёта дисперсии нужны минимум 2 реализации")

    estimates = np.array([
        single_est(sigma_noise, M, R, target_phi)
        for _ in range(K)
    ])

    # Кратчайшая знаковая разность углов.
    errors = (estimates - target_phi + np.pi) % (2 * np.pi) - np.pi

    return np.var(errors, ddof=1)


def variance_vs_phis(sigma_noise, K, M, R, phi_values):
    return [
        calculate_variance(sigma_noise, K, M, R, phi)
        for phi in phi_values
    ]
def calculate_mae(sigma_noise: float, K: int, M, R, target_phi=cfg.target_phi) -> float:
    return sum([single_error(single_est(sigma_noise, M, R, target_phi), target_phi) for _ in range(K)]) / K
def mae_vs_phis(sigma_noise, K, M, R, phi_values):
    
    
    return [calculate_variance(sigma_noise, K, M, R, phi) for phi in phi_values]

def variance_vs_snr(sigma_values, K, M, R):
    """Знеачне ощибки при изменении значения C/Ш"""
    return [calculate_variance(sigma, K, M, R) for sigma in sigma_values]

def variance_vs_sensor_count(sigma, K, M_values, R):
    """Значенеи ошибки при изменении r """
    return [calculate_variance(sigma, K, M, R) for M in M_values]

def variance_vs_radius(sigma, K, M, R_values):
    """Значение ошибки при изменении радиуса решетки"""
    return [calculate_variance(sigma, K, M, R) for R in R_values]

def variance_vs_alpha(sigma, K, M, alpha_values):
    """Значение ошибки при изменении альфа"""
    return [calculate_variance(sigma, K, M, cfg.c/(2*cfg.f*alpha)) for alpha in alpha_values]







