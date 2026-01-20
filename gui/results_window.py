import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SimpleResultsWindow:
    def __init__(self, parent, results, input_data):
        self.parent = parent
        self.results = results
        self.input_data = input_data
        
        self.window = tk.Toplevel(parent)
        self.window.title("Результаты симуляции")
        self.window.geometry("1000x700")
        
        self._create_notebook()
    
    def _create_notebook(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self._create_summary_tab(notebook)
        self._create_trajectory_tab(notebook)
        self._create_thermal_tab(notebook)
        self._create_parachute_tab(notebook)
        
        ttk.Button(self.window, text="Закрыть", 
                  command=self.window.destroy).pack(pady=10)
    
    def _create_summary_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Сводка")
        
        title = ttk.Label(frame, text="Результаты симуляции", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=(10, 5))
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_widget = tk.Text(text_frame, wrap='word', height=20, width=70,
                             font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        summary = self._generate_summary()
        text_widget.insert('1.0', summary)
        text_widget.configure(state='disabled')
    
    def _create_trajectory_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Траектория")
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        
        if hasattr(self.results, 'velocity_total') and hasattr(self.results, 'time'):
            ax = axes[0, 0]
            ax.plot(self.results.time, self.results.velocity_total, 'b-', linewidth=2)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Скорость (м/с)')
            ax.set_title('Зависимость скорости от времени')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        
        if hasattr(self.results, 'height') and hasattr(self.results, 'time'):
            ax = axes[0, 1]
            ax.plot(self.results.time, self.results.height, 'g-', linewidth=2)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Высота (м)')
            ax.set_title('Зависимость высоты от времени')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Поверхность')
            ax.legend()
        
        if hasattr(self.results, 'height') and hasattr(self.results, 'velocity_total'):
            ax = axes[1, 0]
            ax.plot(self.results.height, self.results.velocity_total, 'r-', linewidth=2)
            ax.set_xlabel('Высота (м)')
            ax.set_ylabel('Скорость (м/с)')
            ax.set_title('Зависимость скорости от высоты')
            ax.grid(True, alpha=0.3)
            ax.invert_xaxis()
        
        if hasattr(self.results, 'velocity_x') and hasattr(self.results, 'time'):
            ax = axes[1, 1]
            x_distance = np.zeros_like(self.results.time)
            for i in range(1, len(self.results.time)):
                dt = self.results.time[i] - self.results.time[i-1]
                vx_avg = (self.results.velocity_x[i-1] + self.results.velocity_x[i]) / 2
                x_distance[i] = x_distance[i-1] + vx_avg * dt
            
            ax.plot(x_distance / 1000, self.results.height / 1000, 'm-', linewidth=2)
            ax.set_xlabel('Расстояние (км)')
            ax.set_ylabel('Высота (км)')
            ax.set_title('Траектория полета')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    def _create_thermal_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Тепловые нагрузки")
        
        if not hasattr(self.results, 'heat_flux'):
            label = ttk.Label(frame, text="Тепловые данные отсутствуют", font=("Arial", 12))
            label.pack(pady=50)
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        
        ax = axes[0, 0]
        ax.plot(self.results.time, self.results.heat_flux / 1e6, 'r-', linewidth=2)
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Тепловой поток (МВт/м²)')
        ax.set_title('Тепловой поток на носовой части')
        ax.grid(True, alpha=0.3)
        
        if len(self.results.heat_flux) > 0:
            max_flux = np.max(self.results.heat_flux)
            max_idx = np.argmax(self.results.heat_flux)
            max_time = self.results.time[max_idx]
            ax.plot(max_time, max_flux / 1e6, 'ro', markersize=8, 
                   label=f'Макс: {max_flux/1e6:.1f} МВт/м²')
            ax.legend()
        
        ax = axes[0, 1]
        if len(self.results.time) > 1:
            cumulative = np.zeros(len(self.results.time))
            for i in range(1, len(self.results.time)):
                dt = self.results.time[i] - self.results.time[i-1]
                q_avg = (self.results.heat_flux[i-1] + self.results.heat_flux[i]) / 2
                cumulative[i] = cumulative[i-1] + q_avg * dt
            
            ax.plot(self.results.time, cumulative / 1e6, 'y-', linewidth=2)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Накопленная энергия (МДж/м²)')
            ax.set_title('Накопленная тепловая энергия')
            ax.grid(True, alpha=0.3)
            
            if len(cumulative) > 0:
                final_energy = cumulative[-1]
                ax.text(0.05, 0.95, f'Итого: {final_energy/1e6:.1f} МДж/м²',
                       transform=ax.transAxes, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax = axes[1, 0]
        if hasattr(self.results, 'height'):
            temps = np.where(self.results.height > 70000, 300, 
                           np.where(self.results.height > 40000, 400,
                                   np.where(self.results.height > 10000, 600, 737)))
            ax.plot(self.results.time, temps, 'c-', linewidth=2, label='Температура атмосферы')
        
        if hasattr(self.results, 'thermal_load'):
            tl = self.results.thermal_load
            ax.axhline(y=tl.surface_temperature, color='r', linestyle='--', linewidth=2,
                      label=f'Температура поверхности: {tl.surface_temperature:.0f} K')
            
            if hasattr(self.input_data, 'thermal_properties'):
                melting_temp = self.input_data.thermal_properties.melting_temperature
                ax.axhline(y=melting_temp, color='orange', linestyle=':', linewidth=2,
                          label=f'Температура абляции: {melting_temp:.0f} K')
        
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Температура (K)')
        ax.set_title('Температурные характеристики')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize='small')
        
        ax = axes[1, 1]
        if hasattr(self.results, 'n_exponent'):
            ax.plot(self.results.time, self.results.n_exponent, 'm-', linewidth=2)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Показатель n(v)')
            ax.set_title('Зависимость показателя n от времени')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(1.5, 2.5)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    def _create_parachute_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Парашюты")
        
        if not hasattr(self.results, 'parachute_states'):
            label = ttk.Label(frame, text="Парашютные данные отсутствуют", font=("Arial", 12))
            label.pack(pady=50)
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        
        ax = axes[0, 0]
        states = self.results.parachute_states
        state_values = {'none': 0, 'brake': 1, 'main': 2, 'both': 3}
        numeric_states = [state_values.get(s, 0) for s in states]
        
        ax.step(self.results.time, numeric_states, 'b-', where='post', linewidth=2)
        ax.set_yticks([0, 1, 2, 3])
        ax.set_yticklabels(['Нет', 'Тормозной', 'Основной', 'Оба'])
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Состояние')
        ax.set_title('Состояние парашютной системы')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.5, 3.5)
        
        ax = axes[0, 1]
        ax.plot(self.results.time, self.results.velocity_total, 'g-', linewidth=2)
        
        events = self.results.parachute_events
        event_labels = {
            'brake_deploy': 'Открытие тормозного',
            'main_deploy': 'Открытие основного',
            'brake_jettison': 'Отстрел тормозного'
        }
        
        for event_name, label in event_labels.items():
            time_key = f'{event_name}_time'
            if time_key in events:
                t = events[time_key]
                v = events.get(f'{event_name}_velocity', 0)
                color = 'y' if 'brake' in event_name else 'm'
                marker = '^' if 'deploy' in event_name else 'v'
                ax.plot(t, v, marker=marker, color=color, markersize=10, label=label)
                ax.axvline(x=t, color=color, linestyle=':', alpha=0.5)
        
        ax.set_xlabel('Время (с)')
        ax.set_ylabel('Скорость (м/с)')
        ax.set_title('События парашютов')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize='small')
        
        ax = axes[1, 0]
        if len(self.results.time) > 1:
            acceleration = np.zeros_like(self.results.velocity_total)
            for i in range(1, len(self.results.time)):
                dt = self.results.time[i] - self.results.time[i-1]
                if dt > 0:
                    dv = self.results.velocity_total[i] - self.results.velocity_total[i-1]
                    acceleration[i] = dv / dt
            
            acceleration_g = acceleration / 8.87
            
            ax.plot(self.results.time, acceleration_g, 'r-', linewidth=2)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Перегрузка (g)')
            ax.set_title('Оценка перегрузок')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            
            if len(acceleration_g) > 0:
                max_g = np.max(np.abs(acceleration_g))
                ax.text(0.05, 0.95, f'Макс: {max_g:.1f} g',
                       transform=ax.transAxes, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax = axes[1, 1]
        if hasattr(self.results, 'height'):
            scale_height = 15000
            density_approx = 65.0 * np.exp(-self.results.height / scale_height)
            q_dyn = 0.5 * density_approx * (self.results.velocity_total ** 2)
            
            ax.plot(self.results.time, q_dyn / 1e3, 'b-', linewidth=2)
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Динамическое давление (кПа)')
            ax.set_title('Оценка динамического давления')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    def _generate_summary(self):
        summary = "=" * 60 + "\n"
        summary += "РЕЗУЛЬТАТЫ СИМУЛЯЦИИ ВХОДА В АТМОСФЕРУ ВЕНЕРЫ\n"
        summary += "=" * 60 + "\n\n"
        
        summary += "ПАРАМЕТРЫ ВХОДА:\n"
        summary += "-" * 40 + "\n"
        
        if hasattr(self.input_data, 'entry_height'):
            summary += f"Высота входа: {self.input_data.entry_height/1000:.1f} км\n"
        
        if hasattr(self.input_data, 'entry_speed'):
            summary += f"Скорость входа: {self.input_data.entry_speed:.0f} м/с\n"
        
        if hasattr(self.input_data, 'entry_angle'):
            summary += f"Угол входа: {self.input_data.entry_angle:.1f}°\n"
        
        if hasattr(self.input_data, 'mass_specified'):
            summary += f"Масса аппарата: {self.input_data.mass_specified:.1f} кг\n"
        
        if hasattr(self.input_data, 'drag_coefficient'):
            summary += f"Коэффициент сопротивления: {self.input_data.drag_coefficient:.2f}\n"
        
        if hasattr(self.input_data, 'cross_section_area'):
            summary += f"Площадь сечения: {self.input_data.cross_section_area:.2f} м²\n\n"
        
        summary += "РЕЗУЛЬТАТЫ ПОЛЕТА:\n"
        summary += "-" * 40 + "\n"
        
        if hasattr(self.results, 'flight_time'):
            summary += f"Время полета: {self.results.flight_time:.1f} с\n"
        
        if hasattr(self.results, 'flight_distance'):
            summary += f"Дальность полета: {self.results.flight_distance/1000:.1f} км\n"
        
        if hasattr(self.results, 'final_velocity'):
            summary += f"Конечная скорость: {self.results.final_velocity:.1f} м/с\n"
        
        if hasattr(self.results, 'final_height'):
            summary += f"Конечная высота: {self.results.final_height:.1f} м\n"
        
        if hasattr(self.results, 'angular_displacement'):
            deg = np.degrees(self.results.angular_displacement)
            summary += f"Угловое смещение: {deg:.1f}°\n"
        
        if hasattr(self.results, 'arc_distance'):
            summary += f"Длина дуги: {self.results.arc_distance/1000:.1f} км\n\n"
        
        summary += "ТЕПЛОВЫЕ РЕЗУЛЬТАТЫ:\n"
        summary += "-" * 40 + "\n"
        
        if hasattr(self.results, 'thermal_load'):
            tl = self.results.thermal_load
            summary += f"Макс. тепловой поток: {tl.max_heat_flux/1e6:.2f} МВт/м²\n"
            summary += f"Общая энергия: {tl.total_energy/1e6:.1f} МДж\n"
            summary += f"Энергия на площадь: {tl.energy_per_area/1e6:.1f} МДж/м²\n"
            summary += f"Температура поверхности: {tl.surface_temperature:.0f} K\n"
            if hasattr(tl, 'ablated_fraction'):
                summary += f"Доля аблированного материала: {tl.ablated_fraction*100:.1f}%\n"
            if hasattr(tl, 'ablated_mass'):
                summary += f"Масса аблированного материала: {tl.ablated_mass:.2f} кг\n"
            summary += f"Эффективность теплозащиты: {tl.efficiency:.1f}%\n\n"
        
        summary += "ПАРАШЮТНЫЕ СОБЫТИЯ:\n"
        summary += "-" * 40 + "\n"
        
        events = getattr(self.results, 'parachute_events', {})
        if events:
            for event_name, time in events.items():
                if 'time' in event_name:
                    event_type = event_name.replace('_time', '')
                    velocity = events.get(f'{event_type}_velocity', 'N/A')
                    height = events.get(f'{event_type}_height', 'N/A')
                    
                    event_display = event_type.replace('_', ' ').title()
                    summary += f"{event_display}:\n"
                    summary += f"  Время: {time:.1f} с\n"
                    summary += f"  Скорость: {velocity:.1f} м/с\n"
                    summary += f"  Высота: {height:.1f} м\n"
        else:
            summary += "Парашюты не использовались\n"
        
        return summary