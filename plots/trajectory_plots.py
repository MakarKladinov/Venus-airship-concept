"""
Упрощенные графики траектории
"""
import matplotlib.pyplot as plt
import numpy as np


def plot_speed_height(results):
    """Базовый график скорости и высоты"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Скорость
    ax1.plot(results.time, results.velocity_total, 'b-', label='Полная скорость')
    ax1.set_xlabel('Время (с)')
    ax1.set_ylabel('Скорость (м/с)')
    ax1.set_title('Зависимость скорости от времени')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Высота
    ax2.plot(results.time, results.height, 'g-')
    ax2.set_xlabel('Время (с)')
    ax2.set_ylabel('Высота (м)')
    ax2.set_title('Зависимость высоты от времени')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()


def plot_trajectory(results):
    """График траектории"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Рассчитываем пройденное расстояние
    x_distance = np.zeros_like(results.time)
    for i in range(1, len(results.time)):
        dt = results.time[i] - results.time[i-1]
        vx_avg = (results.velocity_x[i-1] + results.velocity_x[i]) / 2
        x_distance[i] = x_distance[i-1] + vx_avg * dt
    
    # Рисуем траекторию
    ax.plot(x_distance / 1000, results.height / 1000, 'b-')
    ax.set_xlabel('Расстояние (км)')
    ax.set_ylabel('Высота (км)')
    ax.set_title('Траектория полета')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()