import numpy as np
from matplotlib import pyplot as plt
import py_files.config as cfg
import time
import py_files.experiment_stats as es
from collections.abc import Callable

PI_AXIS = { "ticks": np.arange(9) * np.pi / 4,
            "labels": [
                    "0",
                    r"$\frac{\pi}{4}$",
                    r"$\frac{\pi}{2}$",
                    r"$\frac{3\pi}{4}$",
                    r"$\pi$",
                    r"$\frac{5\pi}{4}$",
                    r"$\frac{3\pi}{2}$",
                    r"$\frac{7\pi}{4}$",
                    r"$2\pi$",
                ]
        
    }
COLORS = ["red", "green", "blues"]

def plot_variance_vs_param(est_methods: dict[Callable],
                           config_params: dict,
                           parametr_name: str,
                           title: str,
                           parametr_values: np.ndarray = cfg.SNR_VALUES1,

                           x_size: str = None,
                           y_label: str = r"$s_{\varepsilon}^{2}$",
                           y_size: str = r"$рад$^2$"
                           ):
    """Функция строит график зависимости дисперсии оценки от SNR для двух методов"""
    
    start_time = time.perf_counter()
    vars = {name_func: es.var_vs_params(config_params = config_params,
                                        energy_func = energy_func,
                                        parametr_name = parametr_name,
                                        parametr_values = parametr_values,
                                        phis = cfg.phi_vector) 
                             for name_func, energy_func in est_methods.items()}
        
    end_time = time.perf_counter()
    delta_time = end_time - start_time


    _, ax = plt.subplots(1, 1, figsize=(14, 6), constrained_layout=True)
    for idx, (method, var) in enumerate(vars.items()):
        ax.plot(parametr_values, var, color = COLORS[idx], label =  method)
    if x_size is None:
        x_size = ""
    ax.set_xlabel(parametr_name + x_size, fontsize=18)
    ax.set_ylabel(y_label + y_size, fontsize=18)
    ax.set_title("Зависимость " + y_label + f"от SNR", fontsize=24)
    ax.grid(True)
    ax.legend()

    info = (
        
        f"Центральная частота сигнала: {cfg.f} Гц\n"
        f"Радиус решетки: {round(config_params["R"], 2)}\n"
        f"Количество датчиков: {config_params["M"]}\n"
        f"{parametr_name} от {parametr_values[0]} до {parametr_values[-1]} ({len(parametr_values)} значений)\n\n"
        f"Количество реализаций шума: {config_params["K"]}\n"
        f"Время рассчёта: {round(delta_time,2)} сек."
    )

    ax.text(0.62, 0.96, info, transform=ax.transAxes, fontsize=18, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=1))

  