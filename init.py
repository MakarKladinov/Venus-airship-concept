"""
Пакет venus_atmospheric_simulation

Полная симуляция входа аппарата в атмосферу Венеры
с учетом аэродинамики, тепловых нагрузок и парашютной системы.
"""

__version__ = '1.0.0'
__author__ = 'Venus Simulation Team'
__license__ = 'MIT'

# Импорты для удобного доступа
try:
    from .core.materials import VenusAtmosphere
    from .core.simulation import SimulationEngine, ThermalProperties, ParachuteSystem
    from .gui.main_window import SimpleSimulationApp
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    VenusAtmosphere = None
    SimulationEngine = None
    ThermalProperties = None
    ParachuteSystem = None
    SimpleSimulationApp = None

__all__ = [
    'VenusAtmosphere',
    'SimulationEngine',
    'ThermalProperties',
    'ParachuteSystem',
    'SimpleSimulationApp',
]