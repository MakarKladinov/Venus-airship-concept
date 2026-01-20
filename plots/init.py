"""
Пакет plots - модули для построения графиков
"""

from .trajectory_plots import plot_speed_height, plot_trajectory
from .thermal_plots import plot_heat_flux, plot_temperatures
from .parachute_plots import plot_parachute_events

__all__ = [
    # trajectory plots
    'plot_speed_height',
    'plot_trajectory',
    
    # thermal plots
    'plot_heat_flux',
    'plot_temperatures',
    
    # parachute plots
    'plot_parachute_events',
]