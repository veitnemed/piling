import numpy as np
from matplotlib import pyplot as plt
import py_files.config as cfg
import time
import py_files.experiment_stats as es

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

def plot_variance_vs_param(method_sheme: dict, snr_values: np.ndarray = cfg.SNR_VALUES):
    """Функция строит график зависимости дисперсии оценки от SNR для двух методов"""
    
    start_time = time.perf_counter()
  
    maes = [es.var_vs_snr(energy_func, cfg.f, cfg.STANDART_DIVIATONS_NOISE, cfg.REALESATION_COUNT, cfg.M, cfg.R,phis=cfg.phi_vector) for energy_func in method_sheme.values() ]
    end_time = time.perf_counter()
    delta_time = end_time - start_time


    _, ax = plt.subplots(1, 1, figsize=(14, 6), constrained_layout=True)

    ax.plot(snr_values, maes[0], color = "blue", label =  list(method_sheme.keys())[0])
    ax.plot(snr_values, maes[1], color = "red", label = list(method_sheme.keys())[1])
    ax.set_xlabel("SNR", fontsize=18)
    ax.set_ylabel(r"$s_{\varepsilon}^{2}$" + ", рад$^2$", fontsize=18)
    ax.set_title("Зависимость " + r"$s_{\varepsilon}^{2}$," + " от SNR", fontsize=24)
    ax.grid(True)
    ax.legend()

    info = (
        "Кейпон vs Барлет\n\n"
        f"Центральная частота сигнала: {cfg.f} Гц\n"
        f"Радиус решетки: {round(cfg.R, 2)}\n"
        f"Количество датчиков: {cfg.M}\n"
        f"SNR от {snr_values[0]} до {snr_values[-1]} ({len(snr_values)} значений)\n\n"
        f"Количество реализаций шума: {cfg.REALESATION_COUNT}\n"
        f"Время рассчёта: {round(delta_time,2)} сек."
    )

    ax.text(0.62, 0.96, info, transform=ax.transAxes, fontsize=18, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=1))

  