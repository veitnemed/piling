import numpy as np
import config as cfg

def get_gamma_array(M: int) -> np.ndarray:
    """Рассчет углов датчиков относительно оси x
    Функция принимает на вход число датчиков и возвращает 
    массив углов для каждого датчика"""
    
    return (2*np.pi/M)*np.arange(M)

def get_tau_array(M: int, 
                  R: float, 
                  phi_o: float, 
                  c: float = 343.26) -> np.ndarray:
    """Рассчёт задержек относительно каждого датчика"""
    
    return (R/c)*np.cos(phi_o - get_gamma_array(M))

def get_sin_signal(t: np.ndarray, 
                    f: float,
                    A: float = 1.0,) -> np.ndarray:
    """Считаем значение гармончиеского сигнала в каждый момент времени"""
    
    return  A*np.sin(t*(2*np.pi*f))

def get_noise(scale):
    """Генрация помех"""
    return np.random.normal(loc = 0, scale = scale, size = cfg.N)

def get_avp_signals(
                      p_t: np.ndarray,
                      phi_0: float,
                      noise_level: float = 0) -> dict:
    """Рассчёт y0 y1 y2 для АВП"""
    
    y0 = p_t + get_noise(noise_level) # size (1 x N)
    y1 = p_t*np.cos(phi_0) + get_noise(noise_level)
    y2 = p_t*np.sin(phi_0) + get_noise(noise_level)
        
    return {
        "y0": y0,
        "y1": y1,
        "y2": y2
    }

def get_channel_matrix(
                      t: np.ndarray, 
                      f: float,
                      phi_0: float,
                      tau_array: np.ndarray,
                      M: int,
                      N: int,
                      noise_level: float = cfg.sigma_noise,
                      A: float = 1.0) -> np.ndarray:
    """Функция возращает матрицу 3M x N со значениями для каждого из трёх каналов датчика АВП"""
    
    channel_matrix = np.zeros((3*M, N)) # Создаём нулевую матрицу размера M x N
    for idx, tau in enumerate(tau_array):
        p_t = get_sin_signal(t - tau, f, A)
        signals = get_avp_signals(p_t, phi_0, noise_level)

    
        sensor_matrix = np.vstack((signals["y0"], signals["y1"], signals["y2"])) 
        channel_matrix[idx*3:idx*3+3] = sensor_matrix
        
    return channel_matrix

def get_covariation_matrix(matrix: np.ndarray,
                                N: int) -> np.ndarray:
    return (matrix @ matrix.T) / N

def get_direction_vector(phi_0: float, M: int) -> np.ndarray:
    """Направляющий вектор"""
    return np.array([1,np.cos(phi_0),np.sin(phi_0)]*M).T

def get_barlet_value(phi: float,
                 M: int,
                 W: np.ndarray) -> float:
    """Функция возвращает значение функции Бврлета для одного угла"""
    a = get_direction_vector(phi, M)
    return a.T @ W @ a

def get_barlet_values(phis: np.ndarray,
                 M: int,
                 W: np.ndarray) -> list:
    
    return [get_barlet_value(phi, M, W) for phi in phis]


def score_phi(phi_vector: np.ndarray, e_values: np.ndarray) -> float:
    """Определяем угол по максимум аргумента Барлета"""
    return phi_vector[np.argmax(e_values)]