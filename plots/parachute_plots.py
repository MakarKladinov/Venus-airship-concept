"""
Упрощенные графики парашютов
"""
import matplotlib.pyplot as plt
import numpy as np


def plot_parachute_events(results):
    """График событий парашютов"""
    if not hasattr(results, 'parachute_states'):
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Состояния парашютов
    states = results.parachute_states
    state_values = {'none': 0, 'brake': 1, 'main': 2, 'both': 3}
    numeric_states = [state_values.get(s, 0) for s in states]
    
    ax1.step(results.time, numeric_states, 'b-', where='post')
    ax1.set_yticks([0, 1, 2, 3])
    ax1.set_yticklabels(['Нет', 'Тормозной', 'Основной', 'Оба'])
    ax1.set_xlabel('Время (с)')
    ax1.set_ylabel('Состояние')
    ax1.set_title('Состояние парашютной системы')
    ax1.grid(True, alpha=0.3)
    
    # Скорость с событиями
    ax2.plot(results.time, results.velocity_total, 'g-')
    
    # Отмечаем события
    events = results.parachute_events
    colors = {'brake_deploy': 'y', 'main_deploy': 'm', 'brake_jettison': 'c'}
    
    for event_name, color in colors.items():
        if f'{event_name}_time' in events:
            t = events[f'{event_name}_time']
            v = events.get(f'{event_name}_velocity', 0)
            ax2.plot(t, v, f'{color}^', markersize=10, label=event_name)
            ax2.axvline(x=t, color=color, linestyle=':', alpha=0.5)
    
    ax2.set_xlabel('Время (с)')
    ax2.set_ylabel('Скорость (м/с)')
    ax2.set_title('События парашютов на фоне скорости')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()