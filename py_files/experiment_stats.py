"""Статистика экспериментов"""

import numpy as np
import py_files.config as cfg 
from collections.abc import Callable

from py_files.functions import (
                       get_tau_array,
                       get_covariation_matrix,
                       get_channel_matrix,
                       get_est_phi,
                       get_direction_matrix)


def single_est(config_params: dict,
               dir_matrix: np.ndarray,
               energy_func,
               phis: np.ndarray) -> float:
    """Считаем оценку по одной ревлизации шума"""
    
    tau_array = get_tau_array(config_params)
    channel_matrix = get_channel_matrix(
                                        config_params = config_params,
                                        t = cfg.t, 
                                        tau_array = tau_array)
    W = get_covariation_matrix(channel_matrix, config_params["N"])
    Energy_values = energy_func(W, dir_matrix)
    est = get_est_phi(phis, Energy_values)
    return est

def single_error(est, target_phi):
    """Считаем ошибку оценки по одной ревлизации шума"""
    return (est - target_phi + np.pi)%(2*np.pi) - np.pi

def list_errors(congig_params: dict,
                energy_func,
                phis: np.ndarray
                ) -> float:
    """Формируем список ошибок для каждой реализации шума"""
    dir_matrix = get_direction_matrix(phis, congig_params["M"])
    
    return [single_error(single_est(congig_params, dir_matrix, energy_func, phis), congig_params["target_phi"]) 
            for _ in range(congig_params["K"])]

def calculate_variance(list_errors: list) -> float:
    """Считаем дисперсию по списку ошибок"""
    
    var = 0
    K = len(list_errors)
    m_error = sum(list_errors)/K
    for error in list_errors:
        var += (m_error - error)**2
    return var/(K-1) 

def var_vs_params(config_params: dict,
                  energy_func: Callable,
                  phis: np.ndarray,
                  parametr_name: str,
                  parametr_values: np.ndarray | list):
    """Универсальная фанкция для построения зависимость дисперссии от параметра моделирования"""
    result = []
    config_params = config_params.copy()
    for value in parametr_values:
        if parametr_name not in config_params:
            raise KeyError(F"Неизвестный параметр {parametr_name}")
        config_params[parametr_name] = value
        lst = list_errors(config_params, energy_func,  phis)
        result.append(calculate_variance(lst))
    return result

def var_vs_phis(config_params, energy_func, phis, phi_values):
    result = []
    config_params = config_params.copy()
    for phi  in phi_values:
        config_params["target_phi"] = phi
        lst = list_errors(config_params, energy_func,  phis)
        result.append(calculate_variance(lst))
    return result



def var_vs_alpha_f_const(energy_func, f, sigma, K, M, phis, alpha_values):
    """Значение ошибки при изменении альфа"""
    return [calculate_variance(list_errors(energy_func, f, sigma, K, M, cfg.c/(2*cfg.f*alpha), phis)) for alpha in alpha_values]


def var_vs_alpha_r_const(energy_func, sigma, K, M, alpha_values, phis):
    """Значение ошибки при изменении альфа"""
    return [calculate_variance(list_errors(energy_func, cfg.c/(2*cfg.R1*alpha), sigma, K, M, cfg.R1, phis)) for alpha in alpha_values]



