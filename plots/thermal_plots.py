import matplotlib.pyplot as plt
import numpy as np

def plot_heat_flux(results):
    if not hasattr(results, 'heat_flux'):
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(results.time, results.heat_flux / 1e6, 'r-')
    ax1.set_xlabel('Время (с)')
    ax1.set_ylabel('Тепловой поток (МВт/м²)')
    ax1.set_title('Тепловой поток на носовой части')
    ax1.grid(True, alpha=0.3)
    
    if len(results.time) > 1:
        cumulative = np.zeros(len(results.time))
        for i in range(1, len(results.time)):
            dt = results.time[i] - results.time[i-1]
            q_avg = (results.heat_flux[i-1] + results.heat_flux[i]) / 2
            cumulative[i] = cumulative[i-1] + q_avg * dt
        
        ax2.plot(results.time, cumulative / 1e6, 'orange-')
        ax2.set_xlabel('Время (с)')
        ax2.set_ylabel('Накопленная энергия (МДж/м²)')
        ax2.set_title('Накопленная тепловая энергия')
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_temperatures(results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if hasattr(results, 'atm_temp'):
        ax.plot(results.time, results.atm_temp, 'b-', label='Температура атмосферы')
    
    if hasattr(results, 'thermal_load'):
        tl = results.thermal_load
        ax.axhline(y=tl.surface_temperature, color='r', linestyle='--', 
                  label=f'Температура поверхности: {tl.surface_temperature:.0f} K')
        
        if hasattr(results, 'material_props'):
            mp = results.material_props
            ax.axhline(y=mp.get('melting_temp', 2100), color='orange', linestyle='--',
                      label=f'Температура плавления: {mp.get("melting_temp", 2100)} K')
    
    ax.set_xlabel('Время (с)')
    ax.set_ylabel('Температура (K)')
    ax.set_title('Температурные характеристики')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.show()