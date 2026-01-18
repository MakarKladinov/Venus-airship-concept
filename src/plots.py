import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_speed_height(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': f'Кинематические параметры при входе в атмосферу Венеры (угол: {results["initial_conditions"]["entry_angle"]}°)',
            'speed_time': f'Скорость от времени (угол входа: {results["initial_conditions"]["entry_angle"]:.1f}°)',
            'height_time': 'Высота от времени',
            'surface': 'Поверхность Венеры',
            'v_total': 'Полная скорость',
            'vx': 'Горизонтальная (vx)',
            'vy': 'Вертикальная (vy)',
            'brake_deploy': 'Открытие тормозного',
            'main_deploy': 'Открытие основного',
            'brake_jettison': 'Отстрел тормозного',
            'landing': 'Приземление'
        }
    else:
        titles = {
            'main': f'Kinematic Parameters During Venus Atmospheric Entry (angle: {results["initial_conditions"]["entry_angle"]}°)',
            'speed_time': f'Speed vs Time (entry angle: {results["initial_conditions"]["entry_angle"]:.1f}°)',
            'height_time': 'Height vs Time',
            'surface': 'Venus Surface',
            'v_total': 'Total speed',
            'vx': 'Horizontal (vx)',
            'vy': 'Vertical (vy)',
            'brake_deploy': 'Brake deploy',
            'main_deploy': 'Main deploy',
            'brake_jettison': 'Brake jettison',
            'landing': 'Landing'
        }
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    entry_angle = results['initial_conditions'].get('entry_angle', 20.0)
    vx0 = results['initial_conditions'].get('vx0', 0)
    vy0 = results['initial_conditions'].get('vy0', 0)
    
    ax1.plot(results['time'], results['v_total'], 'b-', linewidth=2, label=titles['v_total'])
    ax1.plot(results['time'], results['vx'], 'r--', linewidth=1.5, alpha=0.7, label=titles['vx'])
    ax1.plot(results['time'], results['vy'], 'g--', linewidth=1.5, alpha=0.7, label=titles['vy'])
    
    if vx0 != 0:
        ax1.plot(0, vx0, 'ro', markersize=8, label=f'vx₀={vx0:.0f} м/с')
    if vy0 != 0:
        ax1.plot(0, vy0, 'go', markersize=8, label=f'vy₀={vy0:.0f} м/с')
    
    if 'parachute_events' in results and results['parachute_events']:
        events = results['parachute_events']
        
        if 'brake_deploy_time' in events:
            t = events['brake_deploy_time']
            v = events['brake_deploy_velocity']
            ax1.plot(t, v, 'y^', markersize=12, label=f'{titles["brake_deploy"]}: {v:.0f} м/с')
            ax1.axvline(x=t, color='y', linestyle=':', alpha=0.5)
        
        if 'main_deploy_time' in events:
            t = events['main_deploy_time']
            v = events['main_deploy_velocity']
            ax1.plot(t, v, 'm^', markersize=12, label=f'{titles["main_deploy"]}: {v:.0f} м/с')
            ax1.axvline(x=t, color='m', linestyle=':', alpha=0.5)
        
        if 'brake_jettison_time' in events:
            t = events['brake_jettison_time']
            v = events['brake_jettison_velocity']
            ax1.plot(t, v, 'c^', markersize=12, label=f'{titles["brake_jettison"]}: {v:.0f} м/с')
            ax1.axvline(x=t, color='c', linestyle=':', alpha=0.5)
    
    if current_lang == 'ru':
        ax1.set_xlabel('Время (с)', fontsize=12)
        ax1.set_ylabel('Скорость (м/с)', fontsize=12)
    else:
        ax1.set_xlabel('Time (s)', fontsize=12)
        ax1.set_ylabel('Speed (m/s)', fontsize=12)
    
    ax1.set_title(titles['speed_time'], fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=9, loc='upper right')
    
    ax2.plot(results['time'], results['height']/1000, 'g-', linewidth=2)
    
    if current_lang == 'ru':
        ax2.set_xlabel('Время (с)', fontsize=12)
        ax2.set_ylabel('Высота (км)', fontsize=12)
    else:
        ax2.set_xlabel('Time (s)', fontsize=12)
        ax2.set_ylabel('Height (km)', fontsize=12)
    
    ax2.set_title(titles['height_time'], fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5, label=titles['surface'])
    
    if 'parachute_events' in results and results['parachute_events']:
        events = results['parachute_events']
        
        if 'brake_deploy_time' in events:
            t = events['brake_deploy_time']
            h = events['brake_deploy_height']/1000
            ax2.plot(t, h, 'y^', markersize=12, label=f'{titles["brake_deploy"]}: {h:.1f} км')
        
        if 'main_deploy_time' in events:
            t = events['main_deploy_time']
            h = events['main_deploy_height']/1000
            ax2.plot(t, h, 'm^', markersize=12, label=f'{titles["main_deploy"]}: {h:.1f} км')
        
        if 'brake_jettison_time' in events:
            t = events['brake_jettison_time']
            h = events['brake_jettison_height']/1000
            ax2.plot(t, h, 'c^', markersize=12, label=f'{titles["brake_jettison"]}: {h:.1f} км')
    
    if len(results['height']) > 0:
        final_h = results['height'][-1]/1000
        final_t = results['time'][-1]
        if final_h < 0.1:
            if current_lang == 'ru':
                ax2.plot(final_t, final_h, 'ro', markersize=8, label=f'Приземление: t={final_t:.1f} с')
            else:
                ax2.plot(final_t, final_h, 'ro', markersize=8, label=f'Landing: t={final_t:.1f} s')
    
    ax2.legend(fontsize=9)
    
    plt.suptitle(titles['main'], fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_heat_flux(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Тепловые нагрузки при входе в атмосферу',
            'heat_flux': 'Тепловой поток на носовой части',
            'cumulative': 'Накопленная тепловая энергия',
            'max': 'Макс',
            'brake': 'Тормозной',
            'main': 'Основной',
            'no_data': 'Нет данных о тепловом потоке',
            'no_cumulative': 'Нет данных о накопленной энергии'
        }
    else:
        titles = {
            'main': 'Thermal Loads During Atmospheric Entry',
            'heat_flux': 'Heat Flux on Nose',
            'cumulative': 'Cumulative Thermal Energy',
            'max': 'Max',
            'brake': 'Brake',
            'main': 'Main',
            'no_data': 'No heat flux data',
            'no_cumulative': 'No cumulative energy data'
        }
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    if len(results['heat_flux']) > 0:
        ax1.plot(results['time'], results['heat_flux']/1e6, 'r-', linewidth=2)
        
        if current_lang == 'ru':
            ax1.set_xlabel('Время (с)', fontsize=12)
            ax1.set_ylabel('Тепловой поток (МВт/м²)', fontsize=12)
        else:
            ax1.set_xlabel('Time (s)', fontsize=12)
            ax1.set_ylabel('Heat Flux (MW/m²)', fontsize=12)
        
        ax1.set_title(titles['heat_flux'], fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        max_idx = np.argmax(results['heat_flux'])
        ax1.plot(results['time'][max_idx], results['heat_flux'][max_idx]/1e6, 
                'ro', markersize=10, label=f'{titles["max"]}: {results["heat_flux"][max_idx]/1e6:.2f} МВт/м²')
        
        if 'parachute_events' in results and results['parachute_events']:
            events = results['parachute_events']
            
            if 'brake_deploy_time' in events:
                t = events['brake_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                q = results['heat_flux'][idx]/1e6
                ax1.plot(t, q, 'y^', markersize=10, label=f'{titles["brake"]}: {q:.2f} МВт/м²')
            
            if 'main_deploy_time' in events:
                t = events['main_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                q = results['heat_flux'][idx]/1e6
                ax1.plot(t, q, 'm^', markersize=10, label=f'{titles["main"]}: {q:.2f} МВт/м²')
        
        ax1.legend(fontsize=9)
    else:
        ax1.text(0.5, 0.5, titles['no_data'], 
                transform=ax1.transAxes, ha='center', va='center', fontsize=12)
        ax1.set_title(titles['heat_flux'], fontsize=14)
    
    if len(results['time']) > 1 and len(results['heat_flux']) > 1:
        q_cumulative = np.zeros_like(results['time'])
        for i in range(1, len(results['time'])):
            dt = results['time'][i] - results['time'][i-1]
            q_cumulative[i] = q_cumulative[i-1] + 0.5*(results['heat_flux'][i] + 
                                                     results['heat_flux'][i-1]) * dt
        
        ax2.plot(results['time'], q_cumulative / 1e6, 'orange', linewidth=2)
        
        if current_lang == 'ru':
            ax2.set_xlabel('Время (с)', fontsize=12)
            ax2.set_ylabel('Накопленная энергия (МДж/м²)', fontsize=12)
        else:
            ax2.set_xlabel('Time (s)', fontsize=12)
            ax2.set_ylabel('Cumulative Energy (MJ/m²)', fontsize=12)
        
        total_heat = q_cumulative[-1]/1e6 if len(q_cumulative) > 0 else 0
        if current_lang == 'ru':
            ax2.set_title(f'Накопленная тепловая энергия (итого: {total_heat:.1f} МДж/м²)', fontsize=14)
        else:
            ax2.set_title(f'Cumulative Thermal Energy (total: {total_heat:.1f} MJ/m²)', fontsize=14)
        
        ax2.grid(True, alpha=0.3)
        
        if 'parachute_events' in results and results['parachute_events']:
            events = results['parachute_events']
            
            if 'brake_deploy_time' in events:
                t = events['brake_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                q = q_cumulative[idx]/1e6
                ax2.plot(t, q, 'y^', markersize=10, label=f'{titles["brake"]}: {q:.1f} МДж/м²')
            
            if 'main_deploy_time' in events:
                t = events['main_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                q = q_cumulative[idx]/1e6
                ax2.plot(t, q, 'm^', markersize=10, label=f'{titles["main"]}: {q:.1f} МДж/м²')
            
            ax2.legend(fontsize=9)
    else:
        ax2.text(0.5, 0.5, titles['no_cumulative'], 
                transform=ax2.transAxes, ha='center', va='center', fontsize=12)
        ax2.set_title(titles['cumulative'], fontsize=14)
    
    plt.suptitle(titles['main'], fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_n_exponent(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Показатель степени сопротивления n(v) = f(v)',
            'n_vs_time': 'Зависимость показателя степени сопротивления от времени',
            'n_vs_speed': 'Зависимость n(v) от скорости',
            'no_n_data': 'Нет данных о показателе n(v)',
            'no_speed_data': 'Нет данных для графика n(v) от скорости',
            'sound_speed': 'Звуковая скорость (340 м/с)'
        }
    else:
        titles = {
            'main': 'Drag Exponent n(v) = f(v)',
            'n_vs_time': 'Drag Exponent vs Time',
            'n_vs_speed': 'n(v) vs Speed',
            'no_n_data': 'No n(v) data',
            'no_speed_data': 'No data for n(v) vs speed plot',
            'sound_speed': 'Sound speed (340 m/s)'
        }
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    if len(results['n_exponent']) > 0:
        ax1.plot(results['time'], results['n_exponent'], 'purple', linewidth=2)
        
        if current_lang == 'ru':
            ax1.set_xlabel('Время (с)', fontsize=12)
            ax1.set_ylabel('n(v)', fontsize=12)
        else:
            ax1.set_xlabel('Time (s)', fontsize=12)
            ax1.set_ylabel('n(v)', fontsize=12)
        
        ax1.set_title(titles['n_vs_time'], fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=2.0, color='b', linestyle='--', alpha=0.5, label='n = 2.0 (гиперзвук)' if current_lang == 'ru' else 'n = 2.0 (hypersonic)')
        ax1.axhline(y=1.65, color='r', linestyle='--', alpha=0.5, label='n = 1.65 (высокие скорости)' if current_lang == 'ru' else 'n = 1.65 (high speed)')
        
        if 'parachute_events' in results and results['parachute_events']:
            events = results['parachute_events']
            
            if 'brake_deploy_time' in events:
                t = events['brake_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                n = results['n_exponent'][idx]
                label = f'Тормозной: n={n:.2f}' if current_lang == 'ru' else f'Brake: n={n:.2f}'
                ax1.plot(t, n, 'y^', markersize=10, label=label)
            
            if 'main_deploy_time' in events:
                t = events['main_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                n = results['n_exponent'][idx]
                label = f'Основной: n={n:.2f}' if current_lang == 'ru' else f'Main: n={n:.2f}'
                ax1.plot(t, n, 'm^', markersize=10, label=label)
        
        ax1.legend(fontsize=9)
    else:
        ax1.text(0.5, 0.5, titles['no_n_data'], 
                transform=ax1.transAxes, ha='center', va='center', fontsize=12)
        ax1.set_title(titles['n_vs_time'], fontsize=14)
    
    if len(results['v_total']) > 0 and len(results['n_exponent']) > 0:
        ax2.plot(results['v_total'], results['n_exponent'], 'go', alpha=0.5, markersize=3)
        
        if current_lang == 'ru':
            ax2.set_xlabel('Скорость (м/с)', fontsize=12)
            ax2.set_ylabel('n(v)', fontsize=12)
        else:
            ax2.set_xlabel('Speed (m/s)', fontsize=12)
            ax2.set_ylabel('n(v)', fontsize=12)
        
        ax2.set_title(titles['n_vs_speed'], fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.axvline(x=340, color='orange', linestyle='--', alpha=0.7, label=titles['sound_speed'])
        
        if 'parachute_events' in results and results['parachute_events']:
            events = results['parachute_events']
            
            if 'brake_deploy_time' in events:
                t = events['brake_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                v = results['v_total'][idx]
                n = results['n_exponent'][idx]
                label = f'Тормозной: v={v:.0f} м/с' if current_lang == 'ru' else f'Brake: v={v:.0f} m/s'
                ax2.plot(v, n, 'y^', markersize=10, label=label)
            
            if 'main_deploy_time' in events:
                t = events['main_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                v = results['v_total'][idx]
                n = results['n_exponent'][idx]
                label = f'Основной: v={v:.0f} м/с' if current_lang == 'ru' else f'Main: v={v:.0f} m/s'
                ax2.plot(v, n, 'm^', markersize=10, label=label)
        
        ax2.legend(fontsize=9)
    else:
        ax2.text(0.5, 0.5, titles['no_speed_data'], 
                transform=ax2.transAxes, ha='center', va='center', fontsize=12)
        ax2.set_title(titles['n_vs_speed'], fontsize=14)
    
    plt.suptitle(titles['main'], fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_trajectory(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Траектория полета',
            'no_data': 'Недостаточно данных для построения траектории',
            'horizontal_dist': 'Горизонтальное расстояние (км)',
            'height': 'Высота (км)',
            'surface': 'Поверхность Венеры',
            'initial_dir': 'Начальное направление',
            'max_heat': 'Макс. нагрев',
            'sound_barrier': 'Звуковой барьер',
            'brake_open': 'Тормозной открыт',
            'main_open': 'Основной открыт'
        }
    else:
        titles = {
            'main': 'Flight Trajectory',
            'no_data': 'Insufficient data for trajectory',
            'horizontal_dist': 'Horizontal Distance (km)',
            'height': 'Height (km)',
            'surface': 'Venus Surface',
            'initial_dir': 'Initial direction',
            'max_heat': 'Max heating',
            'sound_barrier': 'Sound barrier',
            'brake_open': 'Brake open',
            'main_open': 'Main open'
        }
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    if len(results['time']) > 1 and len(results['vx']) > 1:
        x_distance = np.zeros_like(results['time'])
        for i in range(1, len(results['time'])):
            dt = results['time'][i] - results['time'][i-1]
            vx_avg = (results['vx'][i-1] + results['vx'][i]) / 2.0
            x_distance[i] = x_distance[i-1] + vx_avg * dt
        
        x_distance_km = x_distance / 1000
        height_km = results['height'] / 1000
        
        entry_angle = results['initial_conditions'].get('entry_angle', 20.0)
        
        if len(results['v_total']) == len(x_distance_km):
            scatter = ax.scatter(x_distance_km, height_km, 
                               c=results['v_total'], 
                               cmap='plasma', 
                               s=30, alpha=0.7, 
                               edgecolors='k', linewidth=0.5)
        else:
            scatter = ax.scatter(x_distance_km, height_km, 
                               c='blue', 
                               s=30, alpha=0.7, 
                               edgecolors='k', linewidth=0.5)
        
        ax.plot(x_distance_km, height_km, 'k-', alpha=0.3, linewidth=1)
        
        ax.set_xlabel(titles['horizontal_dist'], fontsize=12)
        ax.set_ylabel(titles['height'], fontsize=12)
        
        if current_lang == 'ru':
            ax.set_title(f'Траектория полета (угол: {entry_angle:.1f}°, дальность: {x_distance_km[-1]:.1f} км)', fontsize=14)
        else:
            ax.set_title(f'Flight Trajectory (angle: {entry_angle:.1f}°, range: {x_distance_km[-1]:.1f} km)', fontsize=14)
        
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.7, 
                  label=titles['surface'])
        
        if 'scatter' in locals():
            cbar = plt.colorbar(scatter, ax=ax)
            if current_lang == 'ru':
                cbar.set_label('Скорость (м/с)', fontsize=10)
            else:
                cbar.set_label('Speed (m/s)', fontsize=10)
        
        if len(x_distance_km) > 1 and len(height_km) > 1:
            ax.arrow(x_distance_km[0], height_km[0], 
                    x_distance_km[1] - x_distance_km[0], 
                    height_km[1] - height_km[0], 
                    head_width=5, head_length=2, fc='red', ec='red', alpha=0.7,
                    label=f'{titles["initial_dir"]} ({entry_angle}°)')
        
        if 'heat_flux' in results and len(results['heat_flux']) > 0:
            idx_peak_q = np.argmax(results['heat_flux'])
            if idx_peak_q < len(x_distance_km):
                ax.plot(x_distance_km[idx_peak_q], height_km[idx_peak_q], 
                       'ro', markersize=10, label=titles['max_heat'])
        
        if 'v_total' in results and len(results['v_total']) > 0:
            idx_sound = np.argmin(np.abs(results['v_total'] - 340))
            if idx_sound < len(x_distance_km):
                ax.plot(x_distance_km[idx_sound], height_km[idx_sound], 
                       'go', markersize=10, label=titles['sound_barrier'])
        
        if 'parachute_events' in results and results['parachute_events']:
            events = results['parachute_events']
            
            if 'brake_deploy_time' in events:
                t = events['brake_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                if idx < len(x_distance_km):
                    ax.plot(x_distance_km[idx], height_km[idx], 
                           'y^', markersize=12, label=titles['brake_open'])
            
            if 'main_deploy_time' in events:
                t = events['main_deploy_time']
                idx = np.argmin(np.abs(results['time'] - t))
                if idx < len(x_distance_km):
                    ax.plot(x_distance_km[idx], height_km[idx], 
                           'm^', markersize=12, label=titles['main_open'])
        
        ax.legend(fontsize=9)
    else:
        ax.text(0.5, 0.5, titles['no_data'], 
               transform=ax.transAxes, ha='center', va='center', fontsize=12)
        ax.set_title(titles['main'], fontsize=14)
    
    plt.tight_layout()
    plt.show()

def plot_temperatures(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Температурные характеристики',
            'atm_temp': 'Температура атмосферы Венеры по высоте',
            'surface_temp': 'Расчетная температура теплозащиты',
            'no_atm_data': 'Нет данных о температуре атмосферы',
            'no_surface_data': 'Нет данных о температуре поверхности',
            'no_time_data': 'Нет данных о времени для расчета температуры',
            'atm_temp_label': 'Температура атмосферы',
            'initial': 'Начальная',
            'melting': 'Плавление',
            'max': 'Макс',
            'calculated': 'Расчетная температура поверхности',
            'final': 'Конечная',
            'melting_reached': 'ДОСТИГНУТО ПЛАВЛЕНИЕ'
        }
    else:
        titles = {
            'main': 'Temperature Characteristics',
            'atm_temp': 'Venus Atmospheric Temperature by Height',
            'surface_temp': 'Calculated Heat Shield Temperature',
            'no_atm_data': 'No atmospheric temperature data',
            'no_surface_data': 'No surface temperature data',
            'no_time_data': 'No time data for temperature calculation',
            'atm_temp_label': 'Atmospheric temperature',
            'initial': 'Initial',
            'melting': 'Melting',
            'max': 'Max',
            'calculated': 'Calculated surface temperature',
            'final': 'Final',
            'melting_reached': 'MELTING REACHED'
        }
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    if 'atm_temp' in results and len(results['atm_temp']) > 0:
        ax1.plot(results['time'], results['atm_temp'], 'b-', 
                linewidth=2, label=titles['atm_temp_label'])

        if 'material_props' in results:
            T_initial = results['material_props'].get('T_initial', 20.0)
            T_melt = results['material_props'].get('T_melt', 2100.0)
            T_max = results['material_props'].get('T_max', 2300.0)
        else:
            T_initial = 20.0
            T_melt = 2100.0
            T_max = 2300.0
        
        ax1.axhline(y=T_initial, color='g', linestyle='--', 
                   alpha=0.7, label=f'{titles["initial"]}: {T_initial} K')
        ax1.axhline(y=T_melt, color='r', linestyle='--', 
                   alpha=0.7, label=f'{titles["melting"]}: {T_melt} K')
        ax1.axhline(y=T_max, color='orange', linestyle='--', 
                   alpha=0.7, label=f'{titles["max"]}: {T_max} K')
        
        if current_lang == 'ru':
            ax1.set_xlabel('Время (с)', fontsize=12)
            ax1.set_ylabel('Температура (K)', fontsize=12)
        else:
            ax1.set_xlabel('Time (s)', fontsize=12)
            ax1.set_ylabel('Temperature (K)', fontsize=12)
        
        ax1.set_title(titles['atm_temp'], fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=9)
    else:
        ax1.text(0.5, 0.5, titles['no_atm_data'], 
                transform=ax1.transAxes, ha='center', va='center', fontsize=12)
        ax1.set_title(titles['atm_temp'], fontsize=14)

    if 'surface_temp_final' in results and 'material_props' in results:
        surface_temp_final = results['surface_temp_final']
        T_initial = results['material_props'].get('T_initial', 20.0)
        T_melt = results['material_props'].get('T_melt', 2100.0)
        
        if len(results['time']) > 0:
            time_norm = results['time'] / np.max(results['time'])
            estimated_surface_temp = T_initial + (surface_temp_final - T_initial) * time_norm
            
            ax2.plot(results['time'], estimated_surface_temp, 'r-', 
                    linewidth=2, label=titles['calculated'])
            
            ax2.axhline(y=surface_temp_final, color='b', linestyle='--',
                       alpha=0.7, label=f'{titles["final"]}: {surface_temp_final:.0f} K')
            ax2.axhline(y=T_melt, color='r', linestyle='--', 
                       alpha=0.7, label=f'{titles["melting"]}: {T_melt} K')
            
            if current_lang == 'ru':
                ax2.set_xlabel('Время (с)', fontsize=12)
                ax2.set_ylabel('Температура (K)', fontsize=12)
            else:
                ax2.set_xlabel('Time (s)', fontsize=12)
                ax2.set_ylabel('Temperature (K)', fontsize=12)
            
            if 'delta_T' in results:
                delta_T = results['delta_T']
                if current_lang == 'ru':
                    ax2.set_title(f'Расчетная температура теплозащиты (ΔT = {delta_T:.0f} K)', fontsize=14)
                else:
                    ax2.set_title(f'Calculated Heat Shield Temperature (ΔT = {delta_T:.0f} K)', fontsize=14)
            else:
                ax2.set_title(titles['surface_temp'], fontsize=14)
                
            ax2.grid(True, alpha=0.3)
            ax2.legend(fontsize=9)
            
            if 'melting_reached' in results and results['melting_reached']:
                ax2.text(0.5, 0.9, titles['melting_reached'], 
                        transform=ax2.transAxes, color='red',
                        fontsize=12, fontweight='bold',
                        horizontalalignment='center',
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
            
            if 'parachute_events' in results and results['parachute_events']:
                events = results['parachute_events']
                
                if 'brake_deploy_time' in events:
                    t = events['brake_deploy_time']
                    idx = np.argmin(np.abs(results['time'] - t))
                    temp = estimated_surface_temp[idx]
                    label = f'Тормозной: {temp:.0f} K' if current_lang == 'ru' else f'Brake: {temp:.0f} K'
                    ax2.plot(t, temp, 'y^', markersize=10, label=label)
                
                if 'main_deploy_time' in events:
                    t = events['main_deploy_time']
                    idx = np.argmin(np.abs(results['time'] - t))
                    temp = estimated_surface_temp[idx]
                    label = f'Основной: {temp:.0f} K' if current_lang == 'ru' else f'Main: {temp:.0f} K'
                    ax2.plot(t, temp, 'm^', markersize=10, label=label)
                
                ax2.legend(fontsize=9)
        else:
            ax2.text(0.5, 0.5, titles['no_time_data'], 
                    transform=ax2.transAxes, ha='center', va='center', fontsize=12)
            ax2.set_title(titles['surface_temp'], fontsize=14)
    else:
        ax2.text(0.5, 0.5, titles['no_surface_data'], 
                transform=ax2.transAxes, ha='center', va='center', fontsize=12)
        ax2.set_title(titles['surface_temp'], fontsize=14)
    
    plt.suptitle(titles['main'], fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_orbital_trajectory(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Орбитальные параметры траектории входа в атмосферу Венеры',
            'angular_position': 'Угловое положение аппарата',
            'radial_position': 'Радиальное положение аппарата',
            'azimuthal_speed': 'Азимутальная скорость',
            'radial_speed': 'Радиальная скорость (положительная - к центру)',
            'orbital_trajectory': 'Орбитальная траектория (полярные координаты)',
            'no_angular_data': 'Нет данных об угловом положении',
            'no_radial_data': 'Нет данных о радиальном положении',
            'no_azimuthal_data': 'Нет данных об азимутальной скорости',
            'no_radial_speed_data': 'Нет данных о радиальной скорости',
            'no_polar_data': 'Нет данных для полярного графика',
            'surface': 'Поверхность',
            'time': 'Время (с)',
            'height': 'Высота над поверхностью (км)',
            'angular_coord': 'Угловая координата (град)',
            'azimuthal_speed_label': 'Азимутальная скорость (м/с)',
            'radial_speed_label': 'Радиальная скорость (м/с)'
        }
    else:
        titles = {
            'main': 'Orbital Parameters of Venus Atmospheric Entry Trajectory',
            'angular_position': 'Angular Position',
            'radial_position': 'Radial Position',
            'azimuthal_speed': 'Azimuthal Speed',
            'radial_speed': 'Radial Speed (positive - toward center)',
            'orbital_trajectory': 'Orbital Trajectory (polar coordinates)',
            'no_angular_data': 'No angular position data',
            'no_radial_data': 'No radial position data',
            'no_azimuthal_data': 'No azimuthal speed data',
            'no_radial_speed_data': 'No radial speed data',
            'no_polar_data': 'No data for polar plot',
            'surface': 'Surface',
            'time': 'Time (s)',
            'height': 'Height above surface (km)',
            'angular_coord': 'Angular coordinate (deg)',
            'azimuthal_speed_label': 'Azimuthal Speed (m/s)',
            'radial_speed_label': 'Radial Speed (m/s)'
        }
    
    fig = plt.figure(figsize=(15, 10))
    
    ax1 = plt.subplot(2, 2, 1)
    if 'theta' in results and len(results['theta']) > 0:
        ax1.plot(results['time'], np.degrees(results['theta']), 'b-', linewidth=2)
        ax1.set_xlabel(titles['time'], fontsize=11)
        ax1.set_ylabel(titles['angular_coord'], fontsize=11)
        ax1.set_title(titles['angular_position'], fontsize=12)
        ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, titles['no_angular_data'], 
                transform=ax1.transAxes, ha='center', va='center', fontsize=12)
        ax1.set_title(titles['angular_position'], fontsize=12)
    
    ax2 = plt.subplot(2, 2, 2)
    if 'r' in results and len(results['r']) > 0:
        ax2.plot(results['time'], (results['r'] - 6051800) / 1000, 'g-', linewidth=2)
        ax2.set_xlabel(titles['time'], fontsize=11)
        ax2.set_ylabel(titles['height'], fontsize=11)
        ax2.set_title(titles['radial_position'], fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5, label=titles['surface'])
        ax2.legend(fontsize=9)
    else:
        ax2.text(0.5, 0.5, titles['no_radial_data'], 
                transform=ax2.transAxes, ha='center', va='center', fontsize=12)
        ax2.set_title(titles['radial_position'], fontsize=12)

    ax3 = plt.subplot(2, 2, 3)
    if 'v_theta' in results and len(results['v_theta']) > 0:
        ax3.plot(results['time'], results['v_theta'], 'r-', linewidth=2)
        ax3.set_xlabel(titles['time'], fontsize=11)
        ax3.set_ylabel(titles['azimuthal_speed_label'], fontsize=11)
        ax3.set_title(titles['azimuthal_speed'], fontsize=12)
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, titles['no_azimuthal_data'], 
                transform=ax3.transAxes, ha='center', va='center', fontsize=12)
        ax3.set_title(titles['azimuthal_speed'], fontsize=12)

    ax4 = plt.subplot(2, 2, 4, projection='polar')
    if 'theta' in results and len(results['theta']) > 0 and 'r' in results and len(results['r']) > 0:
        if len(results['r']) > 0:
            r_norm = (results['r'] - np.min(results['r'])) / (np.max(results['r']) - np.min(results['r']))
            scatter = ax4.scatter(results['theta'], r_norm, c=results['v_total'], 
                                 cmap='plasma', s=20, alpha=0.7)
            ax4.set_title(titles['orbital_trajectory'], fontsize=12)
            ax4.grid(True)
            
            cbar = plt.colorbar(scatter, ax=ax4)
            if current_lang == 'ru':
                cbar.set_label('Скорость (м/с)', fontsize=10)
            else:
                cbar.set_label('Speed (m/s)', fontsize=10)
    else:
        ax4.text(0.5, 0.5, titles['no_polar_data'], 
                transform=ax4.transAxes, ha='center', va='center', fontsize=12)
        ax4.set_title(titles['orbital_trajectory'], fontsize=12)
    
    plt.suptitle(titles['main'], fontsize=16)
    plt.tight_layout()
    plt.show()

def plot_3d_trajectory(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': '3D траектория входа в атмосферу Венеры',
            'x_label': 'X (км)',
            'y_label': 'Y (км)',
            'z_label': 'Z (км)',
            'velocity': 'Скорость (нормализованная)',
            'no_data': 'Нет данных для построения 3D траектории',
            'entry_params': 'Параметры входа:',
            'angle': 'Угол',
            'height': 'Высота',
            'speed': 'Скорость',
            'initial_dir': 'Начальное направление'
        }
    else:
        titles = {
            'main': '3D Venus Atmospheric Entry Trajectory',
            'x_label': 'X (km)',
            'y_label': 'Y (km)',
            'z_label': 'Z (km)',
            'velocity': 'Speed (normalized)',
            'no_data': 'No data for 3D trajectory',
            'entry_params': 'Entry parameters:',
            'angle': 'Angle',
            'height': 'Height',
            'speed': 'Speed',
            'initial_dir': 'Initial direction'
        }
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    if 'theta' in results and len(results['theta']) > 0 and 'r' in results and len(results['r']) > 0:
        step = max(1, len(results['theta']) // 200)
        if step < 100:
            step = 100
       
        theta = results['theta'][::step]
        r = results['r'][::step]
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.zeros_like(x)
    
        if 'v_total' in results and len(results['v_total']) == len(results['theta']):
            v_total_subset = results['v_total'][::step]
            v_total_valid = np.array(v_total_subset)
            v_total_valid = np.nan_to_num(v_total_valid, nan=0.0, posinf=0.0, neginf=0.0)
            
            if np.max(v_total_valid) > np.min(v_total_valid):
                colors = (v_total_valid - np.min(v_total_valid)) / (np.max(v_total_valid) - np.min(v_total_valid))
            else:
                colors = v_total_valid
                
            scatter = ax.scatter(x/1000, y/1000, z/1000, 
                               c=colors, cmap='plasma', 
                               s=30, alpha=0.8, 
                               edgecolors='k', linewidth=0.5)
        else:
            scatter = ax.scatter(x/1000, y/1000, z/1000, 
                               c='blue', s=30, alpha=0.8, 
                               edgecolors='k', linewidth=0.5)
        
        ax.plot(x/1000, y/1000, z/1000, 'k-', alpha=0.5, linewidth=1)
        
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        R_venus_km = 6051.8
        
        x_sphere = R_venus_km * np.outer(np.cos(u), np.sin(v))
        y_sphere = R_venus_km * np.outer(np.sin(u), np.sin(v))
        z_sphere = R_venus_km * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_sphere, y_sphere, z_sphere, 
                       color='orange', alpha=0.3,
                       rstride=2, cstride=2, 
                       linewidth=0, antialiased=True,
                       shade=True)
        
        ax.set_xlabel(titles['x_label'], fontsize=12, labelpad=10)
        ax.set_ylabel(titles['y_label'], fontsize=12, labelpad=10)
        ax.set_zlabel(titles['z_label'], fontsize=12, labelpad=10)
        ax.set_title(titles['main'], fontsize=14, pad=20)
  
        
        ax.view_init(elev=30, azim=45) 
        ax.dist = 15  
      
        max_range = np.max([np.ptp(x/1000), np.ptp(y/1000), np.ptp(z/1000)])
        mid_x = (np.max(x/1000) + np.min(x/1000)) * 0.5
        mid_y = (np.max(y/1000) + np.min(y/1000)) * 0.5
        mid_z = (np.max(z/1000) + np.min(z/1000)) * 0.5
        
        ax.set_xlim(mid_x - max_range * 0.8, mid_x + max_range * 0.8)
        ax.set_ylim(mid_y - max_range * 0.8, mid_y + max_range * 0.8)
        ax.set_zlim(mid_z - max_range * 0.8, mid_z + max_range * 0.8)

        if 'scatter' in locals() and hasattr(scatter, 'cmap'):
            cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20, pad=0.1)
            cbar.set_label(titles['velocity'], fontsize=10)

        entry_angle = results['initial_conditions'].get('entry_angle', 20.0)
        h0 = results['initial_conditions'].get('h0', 0)
        v0 = results['initial_conditions'].get('v0_total', 0)
        
        if current_lang == 'ru':
            info_text = f"{titles['entry_params']}\n{titles['angle']}: {entry_angle}°\n{titles['height']}: {h0/1000:.0f} км\n{titles['speed']}: {v0/1000:.1f} км/с"
        else:
            info_text = f"{titles['entry_params']}\n{titles['angle']}: {entry_angle}°\n{titles['height']}: {h0/1000:.0f} km\n{titles['speed']}: {v0/1000:.1f} km/s"
        
        ax.text2D(0.02, 0.98, info_text, transform=ax.transAxes,
                 fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        if len(x) > 1:
            dx = x[1] - x[0]
            dy = y[1] - y[0]
            dz = z[1] - z[0]
            
            scale = 0.1
            ax.quiver(x[0]/1000, y[0]/1000, z[0]/1000,
                     dx/1000 * scale, dy/1000 * scale, dz/1000 * scale,
                     color='red', arrow_length_ratio=0.1, linewidth=2,
                     label=titles['initial_dir'])
        
        ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.9), fontsize=9)
        ax.grid(True, alpha=0.3)
        
    else:
        ax.text2D(0.5, 0.5, titles['no_data'], 
                 transform=ax.transAxes, ha='center', va='center', fontsize=12)
        ax.set_title(titles['main'])
    
    plt.tight_layout()
    plt.show()

def plot_energy_balance(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Баланс тепловой энергии',
            'thermal_energy': 'Тепловая энергия',
            'heat_shield_capacity': 'Емкость теплозащиты',
            'ablation_energy': 'Энергия абляции',
            'efficiency': 'Эффективность',
            'no_data': 'Нет данных об энергиях',
            'energy_unit': 'Энергия (МДж)',
            'melting_reached': 'ДОСТИГНУТО ПЛАВЛЕНИЕ ТЕПЛОЗАЩИТЫ'
        }
    else:
        titles = {
            'main': 'Thermal Energy Balance',
            'thermal_energy': 'Thermal Energy',
            'heat_shield_capacity': 'Heat Shield Capacity',
            'ablation_energy': 'Ablation Energy',
            'efficiency': 'Efficiency',
            'no_data': 'No energy data',
            'energy_unit': 'Energy (MJ)',
            'melting_reached': 'HEAT SHIELD MELTING REACHED'
        }
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    energies = {}
    labels = []
    values = []
    colors = []

    if 'total_heat' in results:
        energies['thermal_energy'] = results['total_heat'] / 1e6
        labels.append(titles['thermal_energy'])
        values.append(energies['thermal_energy'])
        colors.append('red')
    
    if 'energy_capacity' in results:
        energies['heat_shield_capacity'] = results['energy_capacity'] / 1e6
        labels.append(titles['heat_shield_capacity'])
        values.append(energies['heat_shield_capacity'])
        colors.append('green')
    
    if 'melted_mass' in results and results['melted_mass'] > 0:
        if 'material_props' in results:
            L = results['material_props'].get('L', 20e6)
            ablation_energy = results['melted_mass'] * L / 1e6
            energies['ablation_energy'] = ablation_energy
            labels.append(titles['ablation_energy'])
            values.append(ablation_energy)
            colors.append('orange')
    
    if 'heat_shield_efficiency' in results:
        efficiency = results['heat_shield_efficiency']
        labels.append(f"{titles['efficiency']}\n{efficiency:.1f}%")
        efficiency_value = min(energies.get('thermal_energy', 0), 
                             energies.get('heat_shield_capacity', 0)) if energies else 0
        values.append(efficiency_value)
        colors.append('blue')
    
    if values:
        bars = ax.bar(labels, values, color=colors, alpha=0.7)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            if value > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
                       f'{value:.1f} МДж', ha='center', va='bottom', fontsize=10)
        
        ax.set_ylabel(titles['energy_unit'], fontsize=12)
        ax.set_title(titles['main'], fontsize=14)
        ax.set_ylim(0, max(values) * 1.2)
        ax.grid(True, alpha=0.3, axis='y')

        if 'melting_reached' in results and results['melting_reached']:
            ax.text(0.5, 0.95, titles['melting_reached'], 
                   transform=ax.transAxes, ha='center', va='top',
                   fontsize=12, fontweight='bold', color='red',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
        
        legend_text = []
        if energies.get('thermal_energy', 0) > energies.get('heat_shield_capacity', 0):
            if current_lang == 'ru':
                legend_text.append("Теплозащита недостаточна!")
            else:
                legend_text.append("Heat shield insufficient!")
        else:
            if current_lang == 'ru':
                legend_text.append("Теплозащита достаточна")
            else:
                legend_text.append("Heat shield sufficient")
        
        if energies.get('ablation_energy', 0) > 0:
            melted_fraction = results.get('melted_fraction', 0)
            if current_lang == 'ru':
                legend_text.append(f"Расплавлено: {melted_fraction:.1f}%")
            else:
                legend_text.append(f"Melted: {melted_fraction:.1f}%")
        
        if legend_text:
            ax.text(0.02, 0.98, '\n'.join(legend_text), transform=ax.transAxes,
                   verticalalignment='top', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    else:
        ax.text(0.5, 0.5, titles['no_data'], 
               transform=ax.transAxes, ha='center', va='center', fontsize=12)
        ax.set_title(titles['main'], fontsize=14)
    
    plt.tight_layout()
    plt.show()

def plot_parachute_events(results):
    current_lang = results.get('current_lang', 'ru')
    
    if current_lang == 'ru':
        titles = {
            'main': 'Анализ работы парашютной системы',
            'parachute_state': 'Состояние парашютной системы',
            'parachute_params': 'Параметры парашютов',
            'no_data': 'Парашютная система не использовалась',
            'no_params_data': 'Параметры парашютов - нет данных',
            'time': 'Время (с)',
            'parachute_state_label': 'Состояние парашютов',
            'area': 'Площадь (м²)',
            'brake': 'Тормозной',
            'main': 'Основной',
            'brake_info': 'ТОРМОЗНОЙ ПАРАШЮТ:',
            'main_info': 'ОСНОВНОЙ ПАРАШЮТ:',
            'area_label': 'Площадь:',
            'coeff_label': 'Коэф. C:',
            'deploy_label': 'Открытие:',
            'jettison_label': 'Отстрел:',
            'parachutes': 'ПАРАШЮТЫ:',
            'brake_deployed': 'Тормозной открыт:',
            'main_deployed': 'Основной открыт:',
            'brake_jettisoned': 'Тормозной отстрелен:'
        }
        state_labels = ['Нет', 'Тормозной', 'Оба', 'Основной']
    else:
        titles = {
            'main': 'Parachute System Analysis',
            'parachute_state': 'Parachute System State',
            'parachute_params': 'Parachute Parameters',
            'no_data': 'Parachute system not used',
            'no_params_data': 'No parachute parameters data',
            'time': 'Time (s)',
            'parachute_state_label': 'Parachute State',
            'area': 'Area (m²)',
            'brake': 'Brake',
            'main': 'Main',
            'brake_info': 'BRAKE PARACHUTE:',
            'main_info': 'MAIN PARACHUTE:',
            'area_label': 'Area:',
            'coeff_label': 'Coeff C:',
            'deploy_label': 'Deployment:',
            'jettison_label': 'Jettison:',
            'parachutes': 'PARACHUTES:',
            'brake_deployed': 'Brake deployed:',
            'main_deployed': 'Main deployed:',
            'brake_jettisoned': 'Brake jettisoned:'
        }
        state_labels = ['None', 'Brake', 'Both', 'Main']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    if 'parachute_properties' in results and results['parachute_properties']['use_parachute']:
        parachute_props = results['parachute_properties']
        parachute_events = results.get('parachute_events', {})

        if 'parachute_state' in results and len(results['parachute_state']) > 0:
            states = results['parachute_state']
            time = results['time']

            state_values = np.zeros(len(states))
            state_map = {'none': 0, 'brake': 1, 'both': 2, 'main': 3}
            
            for i, state in enumerate(states):
                state_values[i] = state_map.get(state, 0)
            
            ax1.step(time, state_values, 'b-', linewidth=2, where='post')
            ax1.set_xlabel(titles['time'], fontsize=12)
            ax1.set_ylabel(titles['parachute_state_label'], fontsize=12)
            ax1.set_title(titles['parachute_state'], fontsize=14)
            ax1.grid(True, alpha=0.3)
            ax1.set_yticks([0, 1, 2, 3])
            ax1.set_yticklabels(state_labels)

            if parachute_events:
                colors = {'brake_deploy_time': 'y', 
                         'main_deploy_time': 'm', 
                         'brake_jettison_time': 'c'}
                
                for event_name, color in colors.items():
                    if event_name in parachute_events:
                        t = parachute_events[event_name]
                        ax1.axvline(x=t, color=color, linestyle='--', alpha=0.7)

                        if event_name == 'brake_deploy_time':
                            label = 'Тормозной\nоткрыт' if current_lang == 'ru' else 'Brake\ndeployed'
                            ax1.text(t, 3.2, label, 
                                    ha='center', va='bottom', fontsize=9, color='y')
                        elif event_name == 'main_deploy_time':
                            label = 'Основной\nоткрыт' if current_lang == 'ru' else 'Main\ndeployed'
                            ax1.text(t, 3.2, label, 
                                    ha='center', va='bottom', fontsize=9, color='m')
                        elif event_name == 'brake_jettison_time':
                            label = 'Тормозной\nотстрелен' if current_lang == 'ru' else 'Brake\njettisoned'
                            ax1.text(t, 3.2, label, 
                                    ha='center', va='bottom', fontsize=9, color='c')

            state_times = {state_labels[0]: 0, state_labels[1]: 0, 
                          state_labels[2]: 0, state_labels[3]: 0}
            for i in range(len(time) - 1):
                dt = time[i+1] - time[i]
                state_name = state_labels[int(state_values[i])]
                state_times[state_name] += dt
            
            if current_lang == 'ru':
                time_info = f"Время состояний:\n"
            else:
                time_info = f"State times:\n"
            
            for state_name, state_time in state_times.items():
                time_info += f"{state_name}: {state_time:.1f} с\n"
            
            ax1.text(0.02, 0.98, time_info, transform=ax1.transAxes,
                    verticalalignment='top', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        ax2.bar([titles['brake'], titles['main']], 
               [parachute_props['brake_chute_area'], parachute_props['main_chute_area']],
               color=['yellow', 'magenta'], alpha=0.7)
        
        ax2.set_ylabel(titles['area'], fontsize=12)
        ax2.set_title(titles['parachute_params'], fontsize=14)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for i, (name, area) in enumerate([(titles['brake'], parachute_props['brake_chute_area']),
                                         (titles['main'], parachute_props['main_chute_area'])]):
            ax2.text(i, area + max(parachute_props['brake_chute_area'], 
                                  parachute_props['main_chute_area']) * 0.02,
                    f'{area:.0f} м²', ha='center', va='bottom', fontsize=11)
        
        if current_lang == 'ru':
            chute_info = f"""
{titles['brake_info']}
{titles['area_label']} {parachute_props['brake_chute_area']:.0f} м²
{titles['coeff_label']} {parachute_props['brake_chute_coeff']:.2f}
{titles['deploy_label']} {parachute_props['brake_chute_deploy_velocity']:.0f} м/с
{titles['jettison_label']} {parachute_props['brake_chute_jettison_velocity']:.0f} м/с

{titles['main_info']}
{titles['area_label']} {parachute_props['main_chute_area']:.0f} м²
{titles['coeff_label']} {parachute_props['main_chute_coeff']:.2f}
{titles['deploy_label']} {parachute_props['main_chute_deploy_velocity']:.0f} м/с
"""
        else:
            chute_info = f"""
{titles['brake_info']}
{titles['area_label']} {parachute_props['brake_chute_area']:.0f} m²
{titles['coeff_label']} {parachute_props['brake_chute_coeff']:.2f}
{titles['deploy_label']} {parachute_props['brake_chute_deploy_velocity']:.0f} m/s
{titles['jettison_label']} {parachute_props['brake_chute_jettison_velocity']:.0f} m/s

{titles['main_info']}
{titles['area_label']} {parachute_props['main_chute_area']:.0f} m²
{titles['coeff_label']} {parachute_props['main_chute_coeff']:.2f}
{titles['deploy_label']} {parachute_props['main_chute_deploy_velocity']:.0f} m/s
"""
        
        ax2.text(0.02, 0.98, chute_info, transform=ax2.transAxes,
                verticalalignment='top', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        if parachute_events:
            if current_lang == 'ru':
                events_info = f"{titles['parachutes']}\n"
            else:
                events_info = f"{titles['parachutes']}\n"
            
            if 'brake_deploy_time' in parachute_events:
                t = parachute_events['brake_deploy_time']
                v = parachute_events['brake_deploy_velocity']
                h = parachute_events['brake_deploy_height']
                if current_lang == 'ru':
                    events_info += f"{titles['brake_deployed']}\nt={t:.1f} с, v={v:.0f} м/с, h={h/1000:.1f} км\n"
                else:
                    events_info += f"{titles['brake_deployed']}\nt={t:.1f} s, v={v:.0f} m/s, h={h/1000:.1f} km\n"
            
            if 'main_deploy_time' in parachute_events:
                t = parachute_events['main_deploy_time']
                v = parachute_events['main_deploy_velocity']
                h = parachute_events['main_deploy_height']
                if current_lang == 'ru':
                    events_info += f"{titles['main_deployed']}\nt={t:.1f} с, v={v:.0f} м/с, h={h/1000:.1f} км\n"
                else:
                    events_info += f"{titles['main_deployed']}\nt={t:.1f} s, v={v:.0f} m/s, h={h/1000:.1f} km\n"
            
            if 'brake_jettison_time' in parachute_events:
                t = parachute_events['brake_jettison_time']
                v = parachute_events['brake_jettison_velocity']
                h = parachute_events['brake_jettison_height']
                if current_lang == 'ru':
                    events_info += f"{titles['brake_jettisoned']}\nt={t:.1f} с, v={v:.0f} м/с, h={h/1000:.1f} км"
                else:
                    events_info += f"{titles['brake_jettisoned']}\nt={t:.1f} s, v={v:.0f} m/s, h={h/1000:.1f} km"
            
            ax2.text(0.98, 0.98, events_info, transform=ax2.transAxes,
                    verticalalignment='top', horizontalalignment='right', fontsize=8,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    else:
        ax1.text(0.5, 0.5, titles['no_data'], 
                transform=ax1.transAxes, ha='center', va='center', fontsize=12)
        ax1.set_title(titles['parachute_state'], fontsize=14)
        
        ax2.text(0.5, 0.5, titles['no_data'], 
                transform=ax2.transAxes, ha='center', va='center', fontsize=12)
        ax2.set_title(titles['parachute_params'], fontsize=14)
    
    plt.suptitle(titles['main'], fontsize=16)
    plt.tight_layout()
    plt.show()