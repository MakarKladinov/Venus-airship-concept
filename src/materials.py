import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Константы 
R_venus = 6051.8e3  
g0_venus = 8.87     
M_venus = 4.8675e24 
G = 6.67430e-11    


def gravity_at_height(h):
    
    if h < 0:
        return g0_venus
    return g0_venus * (R_venus / (R_venus + h))**2


heights_km = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70,
                       75, 80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 175, 200, 250, 300])
densities_venus = np.array([65.0, 58.0, 50.0, 42.0, 34.0, 26.0, 19.0, 13.0, 8.5, 5.0,
                             2.8, 1.5, 0.8, 0.4, 0.18, 0.08, 0.035, 0.015, 0.006, 0.002,
                             0.001, 0.0004, 1.5e-4, 2.0e-5, 2.5e-6, 3.0e-7, 1.0e-9,
                             1.0e-11, 1.0e-13, 1.0e-15])  


heights_m = heights_km * 1000


log_densities = np.log10(densities_venus)
density_interp_log = interp1d(heights_m, log_densities, kind='cubic', 
                               fill_value=(log_densities[0], log_densities[-1]), 
                               bounds_error=False)

def density_at_height(h):
    
    if h < 0:
        return densities_venus[0]
    elif h > heights_m[-1]:
        
        return 10 ** (log_densities[-1] - (h - heights_m[-1]) / 50000)
    else:
        return 10 ** density_interp_log(h)

def plot_density_profile(max_height: float = 100000):
    
    heights = np.linspace(0, max_height, 1000)
    densities = np.array([density_at_height(h) for h in heights])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    
    ax.plot(densities, heights / 1000, 'b-', linewidth=3, alpha=0.8)
    ax.fill_betweenx(heights / 1000, 0, densities, alpha=0.3, color='blue')
    
    ax.set_xlabel('Плотность атмосферы Венеры, кг/м³', fontsize=14, fontweight='bold')
    ax.set_ylabel('Высота над поверхностью, км', fontsize=14, fontweight='bold')
    ax.set_title('Зависимость плотности атмосферы Венеры от высоты', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xscale('log')
    
    
    key_densities = [1e-2, 1e-1, 1, 10, 50]
    for density in key_densities:
        if density <= np.max(densities) and density >= np.min(densities):
            
            idx = np.argmin(np.abs(densities - density))
            h_key = heights[idx] / 1000
            ax.axvline(x=density, color='gray', linestyle=':', alpha=0.5)
            ax.text(density * 0.8, h_key, f'{density:.0e} кг/м³', 
                   rotation=90, va='center', fontsize=9)
    
    
    key_heights = [0, 20, 40, 60, 80, 100]
    for h in key_heights:
        density = density_at_height(h * 1000)
        if density > 1e-20:
            ax.axhline(y=h, color='gray', linestyle=':', alpha=0.3)
            ax.plot([density], [h], 'ro', markersize=6, alpha=0.7)
            ax.text(density * 3, h + 1, f'{h} км', va='bottom', fontsize=10)
    
    
    info_text = f"""Характеристики атмосферы Венеры:
    
Максимальная плотность: {densities_venus[0]:.1f} кг/м³ (у поверхности)
Минимальная плотность: {densities[-1]:.1e} кг/м³ ({max_height/1000:.0f} км)

Модель: кубическая интерполяция
Диапазон данных: 0-300 км
Экстраполяция: экспоненциальная"""
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            verticalalignment='top', fontsize=11, fontweight='normal',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    
    ax2 = ax.twiny()
    ax2.set_xlabel('Примерное давление, атм (логарифмическая шкала)', 
                  fontsize=12, fontweight='bold', color='red')
    ax2.set_xscale('log')
    
    pressure_approx = densities * 8.314 * 740 / 0.044 / 101325
    ax2.set_xlim(pressure_approx[0], pressure_approx[-1])
    ax2.tick_params(axis='x', colors='red')
    
    plt.tight_layout()
    return fig


temperatures_venus = np.array([737, 700, 663, 627, 590, 553, 516, 480, 443, 406,
                               370, 333, 296, 260, 223, 186, 150, 140, 135, 130,
                               125, 120, 115, 110, 105, 100, 95, 90, 85, 80])  # K

temperature_interp = interp1d(heights_m, temperatures_venus, kind='cubic',
                               fill_value=(temperatures_venus[0], temperatures_venus[-1]),
                               bounds_error=False)

def temperature_at_height(h):
    
    if h < 0:
        return temperatures_venus[0]
    elif h > heights_m[-1]:
        
        return temperatures_venus[-1] - (h - heights_m[-1]) / 10000 * 10
    else:
        return temperature_interp(h)


def speed_of_sound_at_height(h):
    
    T = temperature_at_height(h)
    # CO2: γ = 1.28, R = 188.9 J/(kg·K), M = 0.044 kg/mol
    # c = √(γ * R * T)
    gamma = 1.28  # коэффициент адиабаты для CO2
    R_specific = 188.9  # Дж/(кг·K)
    return np.sqrt(gamma * R_specific * T)

import numpy as np
import matplotlib.pyplot as plt

def n_v(v):

    v0 = 340  
    gamma = 160 
    n_bg = 1.8 
    A = 0.6    
    
   
    lorentz = A / (1 + ((v - v0) / gamma)**2)
    
    if v > 2000:
        decay = np.exp(-(v - 2000) / 3000)
        return n_bg + lorentz * decay
    else:
        return n_bg + lorentz

    
    v_values = np.linspace(0, 8000, 1000)
    n_values = [n_v(v) for v in v_values]

    
    plt.figure(figsize=(10, 6))
    plt.plot(v_values, n_values, 'r-', linewidth=2.5, label='n(v)')

    
    v0 = 340
    n_peak = n_v(v0)
    plt.scatter([v0], [n_peak], color='red', s=100, zorder=5, 
               label=f'Пик: n({v0}) = {n_peak:.2f}')

   
    for y in [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]:
        plt.axhline(y=y, color='gray', linestyle=':', alpha=0.3)

    
    plt.axvline(x=v0, color='blue', linestyle='--', alpha=0.5, 
               label=f'Звуковая скорость ({v0} м/с)')

    
    plt.xlabel('Скорость (м/с)', fontsize=12)
    plt.ylabel('n(v)', fontsize=12)
    plt.title('Резонансная зависимость n(v) с пиком в околозвуковой области', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.ylim(1.3, 2.5)
    plt.xlim(0, 8000)

    plt.tight_layout()
    plt.show()

def pressure_at_height(h):
    
    rho = density_at_height(h)
    T = temperature_at_height(h)
    R_specific = 188.9 
    
    if h == 0:
        return 9.3e6
    
    # P = ρ * R * T
    return rho * R_specific * T

def dynamic_pressure(v, h):
    
    rho = density_at_height(h)
    return 0.5 * rho * v**2

def mach_number(v, h):
    
    c = speed_of_sound_at_height(h)
    return np.abs(v) / c


def orbital_velocity(h):
    
    r = R_venus + h
    return np.sqrt(G * M_venus / r)

def escape_velocity(h):
    
    r = R_venus + h
    return np.sqrt(2 * G * M_venus / r)


def plot_atmospheric_profiles(max_height=150000):
    
    heights = np.linspace(0, max_height, 500)
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Атмосферные характеристики Венеры', fontsize=16, fontweight='bold')
    
    # 1. Плотность
    densities = [density_at_height(h) for h in heights]
    ax = axes[0, 0]
    ax.plot(densities, heights/1000, 'b-', linewidth=2)
    ax.set_xlabel('Плотность, кг/м³')
    ax.set_ylabel('Высота, км')
    ax.set_title('Плотность атмосферы')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=1.225, color='r', linestyle='--', alpha=0.5, label='Земля (у пов.)')
    ax.legend()
    
    # 2. Температура
    temperatures = [temperature_at_height(h) for h in heights]
    ax = axes[0, 1]
    ax.plot(temperatures, heights/1000, 'r-', linewidth=2)
    ax.set_xlabel('Температура, K')
    ax.set_ylabel('Высота, км')
    ax.set_title('Температура атмосферы')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=288, color='b', linestyle='--', alpha=0.5, label='Земля (у пов.)')
    ax.legend()
    
    # 3. Скорость звука
    sound_speeds = [speed_of_sound_at_height(h) for h in heights]
    ax = axes[0, 2]
    ax.plot(sound_speeds, heights/1000, 'g-', linewidth=2)
    ax.set_xlabel('Скорость звука, м/с')
    ax.set_ylabel('Высота, км')
    ax.set_title('Скорость звука в атмосфере')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=340, color='orange', linestyle='--', alpha=0.5, label='Земля (у пов.)')
    ax.legend()
    
    # 4. Гравитация
    gravities = [gravity_at_height(h) for h in heights]
    ax = axes[1, 0]
    ax.plot(gravities, heights/1000, 'purple-', linewidth=2)
    ax.set_xlabel('Ускорение свободного падения, м/с²')
    ax.set_ylabel('Высота, км')
    ax.set_title('Гравитационное ускорение')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=9.81, color='orange', linestyle='--', alpha=0.5, label='Земля (у пов.)')
    ax.legend()
    
    # 5. Давление (оценочное)
    pressures = [pressure_at_height(h) / 1e5 for h in heights]  
    ax = axes[1, 1]
    ax.plot(pressures, heights/1000, 'orange-', linewidth=2)
    ax.set_xlabel('Давление, бар')
    ax.set_ylabel('Высота, км')
    ax.set_title('Атмосферное давление')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    ax.axvline(x=1, color='b', linestyle='--', alpha=0.5, label='Земля (у пов.)')
    ax.legend()
    
    # 6. Орбитальные скорости
    orb_vel = [orbital_velocity(h) / 1000 for h in heights]  
    esc_vel = [escape_velocity(h) / 1000 for h in heights]  
    ax = axes[1, 2]
    ax.plot(orb_vel, heights/1000, 'b-', linewidth=2, label='Орбитальная')
    ax.plot(esc_vel, heights/1000, 'r-', linewidth=2, label='Убегания')
    ax.set_xlabel('Скорость, км/с')
    ax.set_ylabel('Высота, км')
    ax.set_title('Орбитальные скорости')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    return fig, axes

def plot_n_exponent_function():
    
    v = np.linspace(0, 10000, 1000)
    n_values = n_v(v)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(v, n_values, 'b-', linewidth=3)
    ax.fill_between(v, 1.0, n_values, alpha=0.3, color='blue')
    
    
    key_speeds = [0, 340, 1000, 3000, 7000, 10000]
    for speed in key_speeds:
        if speed <= v[-1]:
            n_val = n_v(speed)
            ax.axvline(x=speed, color='gray', linestyle=':', alpha=0.5)
            ax.plot([speed], [n_val], 'ro', markersize=8)
            mach = speed / 340
            ax.text(speed + 50, n_val + 0.02, f'M={mach:.1f}\nv={speed} м/с', 
                   fontsize=9, ha='left')
    
    ax.set_xlabel('Скорость, м/с', fontsize=14, fontweight='bold')
    ax.set_ylabel('Показатель степени n(v)', fontsize=14, fontweight='bold')
    ax.set_title('Зависимость показателя сопротивления от скорости', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    
    ax.axhline(y=2.0, color='r', linestyle='--', alpha=0.7, label='n=2.0 (гиперзвук)')
    ax.axhline(y=1.0, color='g', linestyle='--', alpha=0.7, label='n=1.0 (дозвук)')
    
    
    ax.axvspan(0, 250, alpha=0.1, color='green', label='Дозвуковой')
    ax.axvspan(250, 450, alpha=0.1, color='orange', label='Трансзвуковой')
    ax.axvspan(450, 5000, alpha=0.1, color='red', label='Сверхзвуковой')
    ax.axvspan(5000, 10000, alpha=0.1, color='purple', label='Гиперзвуковой')
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            verticalalignment='top', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    ax.legend(loc='lower right', fontsize=10)
    ax.set_xlim([0, 10000])
    ax.set_ylim([0.8, 2.5])
    
    plt.tight_layout()
    return fig


def calculate_ballistic_coefficient(m, C, A):
    return m / (C * A)

def calculate_deceleration(v, h, ballistic_coeff):
    rho = density_at_height(h)
    n = n_v(v)
    return 0.5 * rho * (v**n) / ballistic_coeff