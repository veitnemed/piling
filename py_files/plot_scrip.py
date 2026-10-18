import numpy as np
from matplotlib import pyplot as plt
import py_files.config as cfg


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
COLORS = ["red", "green", "blue"]

def plot_variance_vs_param(dict_values: dict,
                           config_params: dict,
                           parametr_name: str,
                           ylim: tuple,
                           parametr_values: np.ndarray = cfg.SNR_VALUES,
                           delta_time : float = 0,
                           x_size: str = None,
                           y_label: str = r"$s_{\varepsilon}^{2}$",
                           y_size: str = r", $рад^2$"
                           ):
    """Функция строит график зависимости дисперсии оценки от параметра моделирования
    для двух методов"""
    
    _, ax = plt.subplots(1, 1, figsize=(14, 7), constrained_layout=True)
    for idx, (method, values) in enumerate(dict_values.items()):
        ax.plot(parametr_values, values, color = COLORS[idx], label =  method)
    if x_size is None:
        x_size = ""
    ax.set_xlabel(parametr_name + x_size, fontsize=18)
    ax.set_ylabel(y_label+y_size, fontsize=18)
    ax.set_title("Зависимость " + y_label + f"от {parametr_name}", fontsize=24)
    ax.grid(True)
    ax.set_ylim(ylim)
    ax.legend(fontsize=15)
    s = ""
    for key in list(dict_values.keys()):
        s+=key+" "
    info = (
        f"Методы: {s}\n\n"
        f"Центральная частота сигнала: {config_params["f0"]} Гц\n"
        f"Радиус решетки: {round(config_params["R"], 2)}\n"
        f"Количество датчиков: {config_params["M"]}\n"
        f"{parametr_name} от {parametr_values[0]} до {parametr_values[-1]} ({len(parametr_values)} значений)\n\n"
        f"Количество реализаций шума: {config_params["K"]}\n"
        f"Время рассчёта: {round(delta_time,2)} сек."
    )

    ax.text(0.7, 0.96, info, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=1))

  