import numpy as np
from typing import Tuple, Optional, Dict
from dataclasses import dataclass

# Исправленный импорт - используем относительный импорт
from .materials import VenusAtmosphere, DragExponentModel

@dataclass
class VehicleParameters:
    mass: float
    drag_coefficient: float
    cross_section_area: float
    nose_radius: float
    
    def __post_init__(self):
        if self.nose_radius <= 0 and self.cross_section_area > 0:
            self.nose_radius = np.sqrt(self.cross_section_area / np.pi)

@dataclass
class InitialConditions:
    entry_height: float
    entry_velocity: float
    entry_angle: float
    
    def __post_init__(self):
        angle_rad = np.radians(self.entry_angle)
        self.vx0 = self.entry_velocity * np.cos(angle_rad)
        self.vy0 = -self.entry_velocity * np.sin(angle_rad)

class PhysicsEngine:
    
    def __init__(self,
                 atmosphere: Optional[VenusAtmosphere] = None,
                 drag_model: Optional[DragExponentModel] = None):
        self.atmosphere = atmosphere or VenusAtmosphere()
        self.drag_model = drag_model or DragExponentModel()
    
    def calculate_acceleration(self,
                               vx: float,
                               vy: float,
                               height: float,
                               vehicle: VehicleParameters,
                               parachute_state: str = 'none',
                               parachute_params: Optional[Dict] = None) -> Tuple[float, float, float]:
        v_total = np.sqrt(vx**2 + vy**2)
        
        g = self.atmosphere.gravity(height)
        
        rho = self.atmosphere.density(height)
        
        n = self.drag_model.n_value(v_total)
        
        # Базовое сопротивление аппарата
        if v_total > 1e-3:
            drag_force_magnitude = 0.5 * rho * vehicle.drag_coefficient * \
                                   vehicle.cross_section_area * (v_total ** n)
        else:
            drag_force_magnitude = 0.0
        
        # Добавляем сопротивление парашютов, если они активны
        if parachute_state != 'none' and parachute_params:
            parachute_drag = self._calculate_parachute_drag(
                v_total, rho, parachute_state, parachute_params
            )
            drag_force_magnitude += parachute_drag
        
        if v_total > 1e-3:
            drag_force_x = -drag_force_magnitude * (vx / v_total)
            drag_force_y = -drag_force_magnitude * (vy / v_total)
        else:
            drag_force_x = 0
            drag_force_y = 0
        
        ax = drag_force_x / vehicle.mass
        ay = drag_force_y / vehicle.mass - g
        
        return ax, ay, v_total
    
    def _calculate_parachute_drag(self,
                                 velocity: float,
                                 density: float,
                                 parachute_state: str,
                                 parachute_params: Dict) -> float:
        """Рассчитывает сопротивление парашютов"""
        v_abs = abs(velocity)
        
        total_drag = 0.0
        
        # Тормозной парашют
        if parachute_state in ['brake', 'both']:
            brake_area = parachute_params.get('brake_area', 0)
            brake_coeff = parachute_params.get('brake_coeff', 0.8)
            if brake_area > 0:
                total_drag += 0.5 * density * brake_coeff * brake_area * (v_abs ** 2)
        
        # Основной парашют
        if parachute_state in ['main', 'both']:
            main_area = parachute_params.get('main_area', 0)
            main_coeff = parachute_params.get('main_coeff', 1.2)
            if main_area > 0:
                total_drag += 0.5 * density * main_coeff * main_area * (v_abs ** 2)
        
        return total_drag
    
    # Для обратной совместимости
    def calculate_acceleration_with_parachutes(self,
                                               vx: float,
                                               vy: float,
                                               height: float,
                                               vehicle: VehicleParameters,
                                               parachute_state: str,
                                               parachute_params: Dict) -> Tuple[float, float, float]:
        """Старый метод для обратной совместимости"""
        return self.calculate_acceleration(vx, vy, height, vehicle, 
                                          parachute_state, parachute_params)