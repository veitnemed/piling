import numpy as np
import config as cfg 


from functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_barlet_values,
                       score_phi,
                       get_direction_matrix)




def single_est(sigma_noise, M, R, target_phi, dir_matrix) -> float:
    """Считаем оценку по одной ревлизации шума"""
    
    tau_array = get_tau_array(M, R, target_phi)
    channel_matrix = get_channel_matrix(t=cfg.t, f=cfg.f, phi_0=target_phi, 
                                       tau_array=tau_array, noise_level=sigma_noise, 
                                       A=cfg.A, M=M, N=cfg.N)
    W = get_covariation_matrix(channel_matrix, cfg.N)
    E_barlett = get_barlet_values(W, dir_matrix)
    est = score_phi(cfg.phi_vector, E_barlett)
    return est




def single_error(est, target_phi):
    return (est - target_phi)%(2*np.pi) - np.pi

def list_errors(sigma_noise: float, K: int, M, R, phis, target_phi=cfg.target_phi) -> float:
    dir_matrix = get_direction_matrix(phis, M)
    return [single_error(single_est(sigma_noise, M, R, target_phi, dir_matrix), target_phi) for _ in range(K)]

def calculate_variance(list_errors):
    var = 0
    K = len(list_errors)
    m_error = sum(list_errors)/K
    for error in list_errors:
        var += (m_error - error)**2
    return var/(K-1) 


def var_vs_phis(sigma_noise, K, M, R, phi_values,phis):
    return [calculate_variance(list_errors(sigma_noise, K, M, R, phis, target_phi= phi)) 
            for phi in phi_values]

def var_vs_snr(sigma_values, K, M, R,phis):
    """Знеачне ощибки при изменении значения C/Ш"""
    return [calculate_variance(list_errors(sigma, K, M, R, phis)) for sigma in sigma_values]

def var_vs_sensor_count(sigma, K, M_values, R,phis):
    """Значенеи ошибки при изменении r """
    return [calculate_variance(list_errors(sigma, K, M, R,phis)) for M in M_values]

def var_vs_radius(sigma, K, M, R_values,phis):
    """Значение ошибки при изменении радиуса решетки"""
    return [calculate_variance(list_errors(sigma, K, M, R,phis)) for R in R_values]

def var_vs_alpha(sigma, K, M, alpha_values, phis):
    """Значение ошибки при изменении альфа"""
    return [calculate_variance(list_errors(sigma, K, M, cfg.c/(2*cfg.f*alpha), phis)) for alpha in alpha_values]







