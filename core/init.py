"""
Пакет core - основная логика симуляции
"""

try:
    from .materials import VenusAtmosphere, DragExponentModel, AtmosphericProfile
    from .physics import PhysicsEngine, VehicleParameters, InitialConditions
    from .simulation import SimulationEngine, SimulationInput, SimulationOutput, ParachuteSystem
    from .thermal import ThermalCalculator, ThermalProperties, ThermalLoad
    from .structure import calculate_airship_mass, calculate_heat_shield_mass, calculate_ballistic_coefficient, calculate_nose_radius_from_area
    from .orbital import calculate_orbital_trajectory, calculate_angular_displacement, calculate_arc_distance, calculate_orbital_velocity, calculate_escape_velocity
    
    __all__ = [
        'VenusAtmosphere', 'DragExponentModel', 'AtmosphericProfile',
        'PhysicsEngine', 'VehicleParameters', 'InitialConditions',
        'SimulationEngine', 'SimulationInput', 'SimulationOutput', 'ParachuteSystem',
        'ThermalCalculator', 'ThermalProperties', 'ThermalLoad',
        'calculate_airship_mass', 'calculate_heat_shield_mass', 
        'calculate_ballistic_coefficient', 'calculate_nose_radius_from_area',
        'calculate_orbital_trajectory', 'calculate_angular_displacement', 
        'calculate_arc_distance', 'calculate_orbital_velocity', 
        'calculate_escape_velocity'
    ]
except ImportError as e:
    print(f"Ошибка импорта в core: {e}")
    __all__ = []