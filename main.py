import numpy as np
import matplotlib.pyplot as plt
import config as cfg 

from functions import (get_gamma_array,
                       get_tau_array,
                       get_sin_signal,
                       get_covariation_matrix,
                       get_avp_signals,
                       get_noise,
                       get_channel_matrix,
                       get_barlet_value,
                       get_barlet_values,
                       score_phi)

target_phi = np.pi






def angle_estimation(sigma_noise) -> float:
     
    tau_array = get_tau_array(cfg.M, cfg.R, target_phi)
    channel_matrix = get_channel_matrix(t = cfg.t,
                                    f = cfg.f,
                                    phi_0 = target_phi,
                                    tau_array = tau_array,
                                    noise_level = sigma_noise,
                                    A = cfg.A,
                                    M = cfg.M,
                                    N = cfg.N)
    W = get_covariation_matrix(channel_matrix, cfg. N)
    E_barlett = get_barlet_values(cfg.phi_vector, cfg.M, W)
    est = score_phi(cfg.phi_vector, E_barlett)
    delta = np.abs(target_phi - est)
    return delta

def averaged_estimate(sigma_noise: float, K: int,) -> float:
    return sum([angle_estimation(sigma_noise) for _ in range(K)])/K

def dependence_on_noise_level(sigma_values, K, ):
    return [averaged_estimate(sigma, K) for sigma in sigma_values]

K = 10

snr_values = np.array([0.01, 0.1, 0.2, 1, 2, 5, 10])
sigma_values = cfg.A / snr_values
print(sigma_values)



v = dependence_on_noise_level(sigma_values, K)

plt.plot(snr_values, v)
plt.show()





