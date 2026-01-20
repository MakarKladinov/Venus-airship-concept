"""
Орбитальные расчеты
"""
import numpy as np
from typing import Tuple


def calculate_orbital_trajectory(time: np.ndarray,
                                vx: np.ndarray,
                                vy: np.ndarray,
                                height: np.ndarray,
                                planet_radius: float = 6051800.0) -> Tuple:
    """
    Рассчитывает орбитальные параметры траектории
    
    Args:
        time: массив времени (с)
        vx: массив горизонтальных скоростей (м/с)
        vy: массив вертикальных скоростей (м/с)
        height: массив высот (м)
        planet_radius: радиус планеты (м)
        
    Returns:
        Кортеж орбитальных параметров
    """
    n = len(time)
    if n == 0:
        return (), (), (), (), (), ()
    
    # Инициализация массивов
    theta = np.zeros(n)  # угловое положение, рад
    radius = np.zeros(n)  # расстояние до центра, м
    v_theta = np.zeros(n)  # азимутальная скорость, м/с
    v_r = np.zeros(n)  # радиальная скорость, м/с
    latitude = np.zeros(n)  # широта, рад
    longitude = np.zeros(n)  # долгота, рад
    
    # Начальные условия
    radius[0] = planet_radius + height[0]
    v_r[0] = -vy[0]  # радиальная скорость положительна наружу
    v_theta[0] = vx[0]  # азимутальная скорость
    
    # Интегрирование
    for i in range(n):
        radius[i] = planet_radius + height[i]
        
        # Угловое положение (интегрирование угловой скорости)
        if i == 0:
            theta[0] = 0
        else:
            dt = time[i] - time[i-1]
            if radius[i-1] > 0:
                angular_velocity = vx[i-1] / radius[i-1]
                theta[i] = theta[i-1] + angular_velocity * dt
            else:
                theta[i] = theta[i-1]
        
        # Скорости в сферических координатах
        v_r[i] = -vy[i]  # радиальная скорость (положительная от центра)
        if radius[i] > 0:
            v_theta[i] = vx[i]
        
        # Географические координаты (упрощенно, считаем движение по экватору)
        latitude[i] = 0  # широта 0 - экватор
        longitude[i] = np.degrees(theta[i]) % 360
    
    return theta, radius, v_theta, v_r, latitude, longitude


def calculate_angular_displacement(theta: np.ndarray) -> float:
    """
    Рассчитывает угловое смещение
    
    Args:
        theta: массив угловых положений (рад)
        
    Returns:
        Угловое смещение (рад)
    """
    if len(theta) > 0:
        return theta[-1] - theta[0]
    return 0.0


def calculate_arc_distance(angular_displacement: float,
                          radius: float) -> float:
    """
    Рассчитывает длину дуги траектории
    
    Args:
        angular_displacement: угловое смещение (рад)
        radius: средний радиус (м)
        
    Returns:
        Длина дуги (м)
    """
    return angular_displacement * radius


def calculate_orbital_velocity(height: float,
                              planet_mass: float = 4.8675e24,
                              gravitational_constant: float = 6.67430e-11) -> float:
    """
    Рассчитывает орбитальную скорость
    
    Args:
        height: высота над поверхностью (м)
        planet_mass: масса планеты (кг)
        gravitational_constant: гравитационная постоянная
        
    Returns:
        Орбитальная скорость (м/с)
    """
    radius = 6051800.0 + height  # радиус Венеры + высота
    return np.sqrt(gravitational_constant * planet_mass / radius)


def calculate_escape_velocity(height: float,
                             planet_mass: float = 4.8675e24,
                             gravitational_constant: float = 6.67430e-11) -> float:
    """
    Рассчитывает вторую космическую скорость
    
    Args:
        height: высота над поверхностью (м)
        planet_mass: масса планеты (кг)
        gravitational_constant: гравитационная постоянная
        
    Returns:
        Скорость убегания (м/с)
    """
    radius = 6051800.0 + height
    return np.sqrt(2 * gravitational_constant * planet_mass / radius)