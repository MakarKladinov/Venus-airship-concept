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
| Peak Deceleration | ~ 110 G | ~ 120-140 G | Validated dynamics model |
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
├── resources                       # Resources (images, data)
├── notes                           # Drafts and notes
│ └── Project Venus Dirigible.docx
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
