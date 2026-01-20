# Venus Airship: Atmospheric Entry Simulator & Mission Concept

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

##  Overview

A high-fidelity simulation and concept study for a novel "mother-daughter" buoyant vehicle network designed for long-term exploration of Venus's upper atmosphere ("life layer" at 50-55 km). The project includes a fully functional atmospheric entry simulator, validated against historical mission data.

##  Model Validation Against Venera-13

The core physical models of the simulator have been validated by replicating the descent profile of the **Venera-13** lander. The results show strong agreement with the actual mission data, confirming the accuracy of the atmospheric, aerodynamic, and thermal models.

| Parameter | Simulation Result | Venera-13 Reference | Notes |
| :--- | :--- | :--- | :--- |
| Heat Shield Mass | ~ 211 kg | ~ 220-230 kg | Close match in TPS sizing |
| Peak Deceleration | ~ 137 G | ~ 140-150 G | Validated dynamics model |
| Landing Speed | ~ 6.6 m/s | ~ 7.3 m/s | Validated parachute model |

*This independent validation provides confidence in using this simulator for novel mission concept analysis.*

##  Key Features

*   **Dual Simulation Modes:** Probe entry or buoyant airship with automatic geometry calculation.
*   **Validated Physics:** Models for Venus atmosphere, aerodynamics, heating, and parachute descent.
*   **Concept Innovation:** "Mother-Daughter" airship architecture for extended range and redundancy.
*   **GUI & Visualization:** Intuitive interface and comprehensive plotting tools.

##  Project Structure
```
venus-airship-concept/
├── src                             # Main source code
│
│ ├── core                          # Simulation core
│ │ ├── init.py
│ │ ├── simulation_engine.py
│ │ ├── structure_calculations.py
│ │ ├── thermal_calculations.py
│ │ └── materials.py
│ └── ui                            # User interface
│   ├── init.py
│   ├── gui.py
│   ├── plots.py
│   └── results_window.py
│ 
├── docs                            # Documentation
│ ├── ProjectFormulas.pdf           # Full mathematical model
│ └── DocProg.pdf                   # Program description
│
├── resources                       # Resources (images, data)
│
├── notes                           # Drafts and notes
│ └── Project Venus Dirigible.docx
│
├── .gitignore
├── LICENSE
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MakarKladinov/venus-airship-concept.git
    cd venus-airship-concept
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the simulation GUI:**
    ```bash
    python src/main.py


## Code Structure
'''
ВЕНЕРА-АТМОСФЕРА-СИМУЛЯЦИЯ/
│
├── main.py                         # Точка входа в приложение
│   └── main()                      # Запуск GUI приложения
│
├── init.py                         # Основной пакет
│   └── Импорты всех основных классов
│
├── core/
│   ├── init.py                     # Основные модули симуляции
│   │   └── Импорты всех core модулей
│   │
│   ├── materials.py                # Модели атмосферы Венеры
│   │   ├── AtmosphericConstants    # Константы атмосферы
│   │   ├── VenusAtmosphere         # Модель атмосферы
│   │   │   ├── __init__()
│   │   │   ├── _init_density_profile()
│   │   │   ├── _init_temperature_profile()
│   │   │   ├── density(height)
│   │   │   ├── temperature(height)
│   │   │   ├── gravity(height)
│   │   │   ├── pressure(height)
│   │   │   ├── sound_speed(height)
│   │   │   ├── mach_number(velocity, height)
│   │   │   ├── dynamic_pressure(velocity, height)
│   │   │   ├── orbital_velocity(height)
│   │   │   └── escape_velocity(height)
│   │   │
│   │   ├── DragExponentModel       # Модель переменного показателя сопротивления
│   │   │   ├── __init__(v0, gamma, n_background, amplitude)
│   │   │   ├── n_value(velocity)
│   │   │   └── flight_regime(velocity)
│   │   │
│   │   └── AtmosphericProfile      # Профиль атмосферных параметров
│   │       ├── create(atmosphere, max_height, num_points)
│   │       └── plot_density_profile(ax)
│   │
│   ├── physics.py                  # Физические расчеты
│   │   ├── VehicleParameters       # Параметры аппарата
│   │   │   └── __post_init__()
│   │   │
│   │   ├── InitialConditions       # Начальные условия
│   │   │   └── __post_init__()
│   │   │
│   │   └── PhysicsEngine           # Движок физических расчетов
│   │       ├── __init__(atmosphere, drag_model)
│   │       ├── calculate_acceleration(vx, vy, height, vehicle)
│   │       ├── calculate_acceleration_with_parachutes(vx, vy, height, vehicle, parachute_state, parachute_params)
│   │       ├── calculate_trajectory_distance(time, vx)
│   │       └── calculate_ballistic_coefficient(vehicle)
│   │
│   ├── thermal.py                  # Тепловые расчеты
│   │   ├── ThermalProperties       # Тепловые свойства материала
│   │   │
│   │   ├── ThermalLoad             # Тепловая нагрузка
│   │   │
│   │   └── ThermalCalculator       # Калькулятор тепловых нагрузок
│   │       ├── calculate_heat_flux(velocity, density, drag_coefficient)
│   │       ├── calculate_total_energy(time, heat_flux, heat_shield_area)
│   │       ├── calculate_simple_temperature(energy_per_area, properties)
│   │       ├── calculate_temperature_with_melting(energy_per_area, properties)
│   │       ├── calculate_efficiency(total_energy, properties)
│   │       └── calculate_heat_shield_mass(properties)
│   │
│   ├── structure.py                # Расчет конструкций
│   │   ├── calculate_airship_mass(envelope_density, payload_mass, gas_lift, heat_shield_thickness, heat_shield_density, heat_shield_area)
│   │   ├── calculate_heat_shield_mass(density, thickness, area)
│   │   ├── calculate_ballistic_coefficient(mass, drag_coefficient, cross_section_area)
│   │   └── calculate_nose_radius_from_area(cross_section_area)
│   │
│   ├── orbital.py                  # Орбитальные расчеты
│   │   ├── calculate_orbital_trajectory(time, vx, vy, height, planet_radius)
│   │   ├── calculate_angular_displacement(theta)
│   │   ├── calculate_arc_distance(angular_displacement, radius)
│   │   ├── calculate_orbital_velocity(height, planet_mass, gravitational_constant)
│   │   └── calculate_escape_velocity(height, planet_mass, gravitational_constant)
│   │
│   └── simulation.py               # Движок симуляции
│       ├── ParachuteSystem         # Парашютная система
│       │
│       ├── SimulationInput         # Входные данные
│       │
│       ├── SimulationOutput        # Выходные данные
│       │
│       └── SimulationEngine        # Движок симуляции
│           ├── __init__()
│           ├── run(input_data, progress_callback)
│           ├── _calculate_vehicle_mass(input_data)
│           ├── _integrate_trajectory(init_conditions, vehicle, input_data, progress_callback)
│           ├── _determine_parachute_state(velocity, parachute_system, brake_deployed, main_deployed, brake_jettisoned, events, time, height)
│           ├── _calculate_thermal_loads(trajectory_results, input_data)
│           └── _compile_output(trajectory_results, thermal_load, orbital_results, input_data, vehicle_mass, airship_results, init_conditions)
│
├── gui/
│   ├── init.py                     # Графический интерфейс
│   │   └── Импорты GUI модулей
│   │
│   ├── main_window.py              # Главное окно
│   │   └── SimpleSimulationApp     # Упрощенный интерфейс
│   │       ├── __init__(root)
│   │       ├── _get_default_params()
│   │       ├── _create_simple_interface()
│   │       ├── _calculate_velocity_components()
│   │       ├── _reset_to_defaults()
│   │       ├── _get_simulation_input()
│   │       ├── _start_simulation()
│   │       ├── _run_simulation_thread(input_data)
│   │       ├── _update_progress(percent, message)
│   │       ├── _show_results(results, input_data)
│   │       ├── _generate_simple_summary(results)
│   │       ├── _show_error(error_message)
│   │       └── _simulation_finished()
│   │
│   └── results_window.py           # Окно результатов
│       └── SimpleResultsWindow     # Окно с графиками
│           ├── __init__(parent, results, input_data)
│           ├── _create_notebook()
│           ├── _create_summary_tab(notebook)
│           ├── _create_trajectory_tab(notebook)
│           ├── _create_thermal_tab(notebook)
│           ├── _create_parachute_tab(notebook)
│           └── _generate_summary()
│
└── plots/                          # (ОПЦИОНАЛЬНО) Модули графиков
    ├── init.py                     # Импорты графиков
    │
    ├── trajectory_plots.py         # Графики траектории
    │   ├── plot_speed_height(results)
    │   └── plot_trajectory(results)
    │
    ├── thermal_plots.py            # Тепловые графики
    │   ├── plot_heat_flux(results)
    │   └── plot_temperatures(results)
    │
    └── parachute_plots.py          # Графики парашютов
        └── plot_parachute_events(results)
'''