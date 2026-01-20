"""
Модели атмосферы Венеры
"""
import numpy as np
from typing import Tuple, Optional, List
from dataclasses import dataclass
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


@dataclass
class AtmosphericConstants:
    """Константы атмосферы Венеры"""
    # Радиус Венеры, м
    RADIUS: float = 6051.8e3
    
    # Ускорение свободного падения у поверхности, м/с²
    GRAVITY_SURFACE: float = 8.87
    
    # Масса Венеры, кг
    MASS: float = 4.8675e24
    
    # Гравитационная постоянная, Н·м²/кг²
    G: float = 6.67430e-11
    
    # Удельная газовая постоянная для CO2, Дж/(кг·K)
    R_SPECIFIC_CO2: float = 188.9
    
    # Коэффициент адиабаты для CO2
    GAMMA_CO2: float = 1.28
    
    # Плотность у поверхности, кг/м³
    DENSITY_SURFACE: float = 65.0
    
    # Температура у поверхности, K
    TEMPERATURE_SURFACE: float = 737
    
    # Давление у поверхности, Па
    PRESSURE_SURFACE: float = 9.3e6


class VenusAtmosphere:
    """Модель атмосферы Венеры"""
    
    def __init__(self):
        self.constants = AtmosphericConstants()
        self._init_density_profile()
        self._init_temperature_profile()
    
    def _init_density_profile(self):
        """Инициализация профиля плотности"""
        # Данные о плотности на разных высотах (км → кг/м³)
        heights_km = np.array([
            0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70,
            75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 175, 200, 250, 300
        ])
        
        densities = np.array([
            65.0, 58.0, 50.0, 42.0, 34.0, 26.0, 19.0, 13.0, 8.5, 5.0,
            2.8, 1.5, 0.8, 0.4, 0.18, 0.08, 0.035, 0.015, 0.006, 0.002,
            0.001, 0.0004, 1.5e-4, 2.0e-5, 2.5e-6, 3.0e-7, 1.0e-9,
            1.0e-11, 1.0e-13, 1.0e-15
        ])
        
        self._heights_m = heights_km * 1000
        self._densities = densities
        
        # Логарифмическая интерполяция для большей точности
        log_densities = np.log10(densities)
        self._density_interp = interp1d(
            self._heights_m, log_densities,
            kind='cubic',
            fill_value=(log_densities[0], log_densities[-1]),
            bounds_error=False
        )
    
    def _init_temperature_profile(self):
        """Инициализация профиля температуры"""
        temperatures = np.array([
            737, 700, 663, 627, 590, 553, 516, 480, 443, 406,
            370, 333, 296, 260, 223, 186, 150, 140, 135, 130,
            125, 120, 115, 110, 105, 100, 95, 90, 85, 80
        ])
        
        self._temperature_interp = interp1d(
            self._heights_m, temperatures,
            kind='cubic',
            fill_value=(temperatures[0], temperatures[-1]),
            bounds_error=False
        )
    
    def density(self, height: float) -> float:
        """
        Плотность атмосферы на заданной высоте
        
        Args:
            height: Высота над поверхностью (м)
            
        Returns:
            Плотность (кг/м³)
        """
        if height < 0:
            return self._densities[0]
        elif height > self._heights_m[-1]:
            # Экстраполяция: экспоненциальный спад
            last_height = self._heights_m[-1]
            last_density = self._densities[-1]
            scale_height = 50000  # м, характерная высота
            return last_density * np.exp(-(height - last_height) / scale_height)
        else:
            return 10 ** self._density_interp(height)
    
    def temperature(self, height: float) -> float:
        """
        Температура на заданной высоте
        
        Args:
            height: Высота над поверхностью (м)
            
        Returns:
            Температура (K)
        """
        if height < 0:
            return self._temperature_interp(0)
        elif height > self._heights_m[-1]:
            return self._temperature_interp(self._heights_m[-1])
        else:
            return float(self._temperature_interp(height))
    
    def gravity(self, height: float) -> float:
        """
        Ускорение свободного падения на заданной высоте
        
        Args:
            height: Высота над поверхностью (м)
            
        Returns:
            Ускорение свободного падения (м/с²)
        """
        if height < 0:
            return self.constants.GRAVITY_SURFACE
        
        r = self.constants.RADIUS + height
        return self.constants.GRAVITY_SURFACE * (self.constants.RADIUS / r) ** 2
    
    def pressure(self, height: float) -> float:
        """
        Давление на заданной высоте (оценочное)
        
        Args:
            height: Высота над поверхностью (м)
            
        Returns:
            Давление (Па)
        """
        if height == 0:
            return self.constants.PRESSURE_SURFACE
        
        rho = self.density(height)
        T = self.temperature(height)
        return rho * self.constants.R_SPECIFIC_CO2 * T
    
    def sound_speed(self, height: float) -> float:
        """
        Скорость звука на заданной высоте
        
        Args:
            height: Высота над поверхностью (м)
            
        Returns:
            Скорость звука (м/с)
        """
        T = self.temperature(height)
        return np.sqrt(self.constants.GAMMA_CO2 * self.constants.R_SPECIFIC_CO2 * T)
    
    def mach_number(self, velocity: float, height: float) -> float:
        """
        Число Маха для заданной скорости и высоты
        
        Args:
            velocity: Скорость (м/с)
            height: Высота (м)
            
        Returns:
            Число Маха
        """
        c = self.sound_speed(height)
        if c > 0:
            return abs(velocity) / c
        return 0.0
    
    def dynamic_pressure(self, velocity: float, height: float) -> float:
        """
        Динамическое давление
        
        Args:
            velocity: Скорость (м/с)
            height: Высота (м)
            
        Returns:
            Динамическое давление (Па)
        """
        rho = self.density(height)
        return 0.5 * rho * velocity ** 2
    
    def orbital_velocity(self, height: float) -> float:
        """
        Орбитальная скорость на заданной высоте
        
        Args:
            height: Высота (м)
            
        Returns:
            Орбитальная скорость (м/с)
        """
        r = self.constants.RADIUS + height
        return np.sqrt(self.constants.G * self.constants.MASS / r)
    
    def escape_velocity(self, height: float) -> float:
        """
        Вторая космическая скорость на заданной высоте
        
        Args:
            height: Высота (м)
            
        Returns:
            Скорость убегания (м/с)
        """
        r = self.constants.RADIUS + height
        return np.sqrt(2 * self.constants.G * self.constants.MASS / r)


class DragExponentModel:
    """Модель переменного показателя степени сопротивления"""
    
    def __init__(self, v0: float = 340.0, gamma: float = 160.0,
                 n_background: float = 1.8, amplitude: float = 0.6):
        """
        Args:
            v0: Резонансная скорость (м/с)
            gamma: Ширина резонанса (м/с)
            n_background: Фоновое значение показателя n
            amplitude: Амплитуда резонанса
        """
        self.v0 = v0
        self.gamma = gamma
        self.n_background = n_background
        self.amplitude = amplitude
    
    def n_value(self, velocity: float) -> float:
        """
        Показатель степени n(v) для заданной скорости
        
        Args:
            velocity: Скорость (м/с)
            
        Returns:
            Показатель степени n
        """
        v_abs = abs(velocity)
        
        # Лоренцев профиль резонанса
        lorentz = self.amplitude / (1 + ((v_abs - self.v0) / self.gamma) ** 2)
        
        # Экспоненциальный спад на высоких скоростях
        if v_abs > 2000:
            decay = np.exp(-(v_abs - 2000) / 3000)
            return self.n_background + lorentz * decay
        else:
            return self.n_background + lorentz
    
    def flight_regime(self, velocity: float) -> str:
        """
        Определяет режим полета по скорости
        
        Args:
            velocity: Скорость (м/с)
            
        Returns:
            Режим полета
        """
        v_abs = abs(velocity)
        
        if v_abs < 250:
            return "subsonic"
        elif 250 <= v_abs < 450:
            return "transonic"
        elif 450 <= v_abs < 5000:
            return "supersonic"
        else:
            return "hypersonic"


@dataclass
class AtmosphericProfile:
    """Профиль атмосферных параметров"""
    heights: np.ndarray
    densities: np.ndarray
    temperatures: np.ndarray
    pressures: np.ndarray
    sound_speeds: np.ndarray
    gravities: np.ndarray
    
    @classmethod
    def create(cls, atmosphere: VenusAtmosphere,
               max_height: float = 100000,
               num_points: int = 1000) -> 'AtmosphericProfile':
        """
        Создает профиль атмосферных параметров
        
        Args:
            atmosphere: Объект атмосферы
            max_height: Максимальная высота (м)
            num_points: Количество точек
            
        Returns:
            AtmosphericProfile
        """
        heights = np.linspace(0, max_height, num_points)
        
        densities = np.array([atmosphere.density(h) for h in heights])
        temperatures = np.array([atmosphere.temperature(h) for h in heights])
        pressures = np.array([atmosphere.pressure(h) for h in heights])
        sound_speeds = np.array([atmosphere.sound_speed(h) for h in heights])
        gravities = np.array([atmosphere.gravity(h) for h in heights])
        
        return cls(heights, densities, temperatures, pressures, sound_speeds, gravities)
    
    def plot_density_profile(self, ax=None):
        """Построение графика плотности"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(self.densities, self.heights / 1000, 'b-', linewidth=3, alpha=0.8)
        ax.fill_betweenx(self.heights / 1000, 0, self.densities, alpha=0.3, color='blue')
        
        ax.set_xlabel('Плотность атмосферы, кг/м³', fontsize=14)
        ax.set_ylabel('Высота над поверхностью, км', fontsize=14)
        ax.set_title('Зависимость плотности атмосферы Венеры от высоты', fontsize=16)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xscale('log')
        
        return ax