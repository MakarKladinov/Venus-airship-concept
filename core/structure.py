"""
Расчет конструкций (дирижабль, теплозащита и т.д.)
"""
import numpy as np
from typing import Dict


def calculate_airship_mass(envelope_density: float,
                          payload_mass: float,
                          gas_lift: float,
                          heat_shield_thickness: float,
                          heat_shield_density: float,
                          heat_shield_area: float) -> Dict[str, float]:
    """
    Рассчитывает параметры аппарата как дирижабля
    
    Args:
        envelope_density: плотность оболочки (кг/м³)
        payload_mass: масса полезной нагрузки (кг)
        gas_lift: подъемная сила газа (кг/м³)
        heat_shield_thickness: толщина теплозащиты (м)
        heat_shield_density: плотность теплозащиты (кг/м³)
        heat_shield_area: площадь теплозащиты (м²)
        
    Returns:
        Словарь с параметрами дирижабля
    """
    # Масса теплозащиты
    heat_shield_mass = heat_shield_density * heat_shield_thickness * heat_shield_area
    
    # Начальная оценка радиуса
    if gas_lift <= 0:
        R = 5.0  # радиус по умолчанию
    else:
        # Итерационный расчет радиуса
        R = (payload_mass / (gas_lift * (4.0/3.0) * np.pi)) ** (1.0/3.0)
        
        for _ in range(10):  # 10 итераций для сходимости
            surface_area = 4.0 * np.pi * R ** 2
            envelope_mass = envelope_density * surface_area
            total_mass_for_lift = envelope_mass + payload_mass
            R_new = (total_mass_for_lift / (gas_lift * (4.0/3.0) * np.pi)) ** (1.0/3.0)
            
            if abs(R_new - R) < 0.01:  # критерий сходимости
                break
            R = R_new
    
    # Гарантируем минимальный радиус
    R = max(R, 0.5)
    
    # Геометрические параметры
    volume = (4.0/3.0) * np.pi * R ** 3
    surface_area = 4.0 * np.pi * R ** 2
    
    # Массы
    envelope_mass = envelope_density * surface_area
    total_mass_for_lift = envelope_mass + payload_mass
    total_mass = total_mass_for_lift + heat_shield_mass
    
    # Силы
    lift_force = gas_lift * volume * 9.81  # Н
    weight_force = total_mass_for_lift * 9.81  # Н
    
    return {
        'total_mass': total_mass,
        'volume': volume,
        'radius': R,
        'envelope_mass': envelope_mass,
        'heat_shield_mass': heat_shield_mass,
        'surface_area': surface_area,
        'lift_force': lift_force,
        'weight_force': weight_force,
        'payload_mass': payload_mass,
        'total_mass_for_lift': total_mass_for_lift,
        'envelope_density': envelope_density,
        'gas_lift': gas_lift
    }


def calculate_heat_shield_mass(density: float,
                              thickness: float,
                              area: float) -> float:
    """
    Рассчитывает массу теплозащиты
    
    Args:
        density: плотность материала (кг/м³)
        thickness: толщина (м)
        area: площадь (м²)
        
    Returns:
        Масса теплозащиты (кг)
    """
    return density * thickness * area


def calculate_ballistic_coefficient(mass: float,
                                   drag_coefficient: float,
                                   cross_section_area: float) -> float:
    """
    Рассчитывает баллистический коэффициент
    
    Args:
        mass: масса (кг)
        drag_coefficient: коэффициент сопротивления
        cross_section_area: площадь сечения (м²)
        
    Returns:
        Баллистический коэффициент
    """
    if drag_coefficient > 0 and cross_section_area > 0:
        return mass / (drag_coefficient * cross_section_area)
    return float('inf')


def calculate_nose_radius_from_area(cross_section_area: float) -> float:
    """
    Рассчитывает радиус носовой части из площади сечения
    
    Args:
        cross_section_area: площадь сечения (м²)
        
    Returns:
        Радиус носовой части (м)
    """
    if cross_section_area > 0:
        return np.sqrt(cross_section_area / np.pi)
    return 0.5  # значение по умолчанию