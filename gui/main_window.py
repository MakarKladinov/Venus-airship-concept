
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import numpy as np

# Исправленный импорт
try:
    from core.simulation import SimulationEngine, SimulationInput, ThermalProperties, ParachuteSystem
    from gui.results_window import SimpleResultsWindow
except ImportError:
    # Альтернативный вариант импорта
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.simulation import SimulationEngine, SimulationInput, ThermalProperties, ParachuteSystem
    from gui.results_window import SimpleResultsWindow

class SimpleSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Симуляция входа в атмосферу Венеры")
        self.root.geometry("900x700")
        
        self.simulation_engine = SimulationEngine()
        self.running = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Создаем основную рамку с прокруткой
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Создаем Canvas для прокрутки
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Теперь создаем виджеты внутри scrollable_frame
        content_frame = ttk.Frame(scrollable_frame, padding="10")
        content_frame.pack(fill='both', expand=True)
        
        title = ttk.Label(content_frame, text="Симуляция входа в атмосферу Венеры", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        row = 1
        
        # Параметры входа
        ttk.Label(content_frame, text="Высота входа (км):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.entry_height = ttk.Entry(content_frame, width=15)
        self.entry_height.insert(0, "250")
        self.entry_height.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(content_frame, text="(50-300 км)").grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Скорость входа (м/с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.entry_speed = ttk.Entry(content_frame, width=15)
        self.entry_speed.insert(0, "7500")
        self.entry_speed.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(content_frame, text="(1000-12000 м/с)").grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Угол входа (градусы):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.entry_angle = ttk.Entry(content_frame, width=15)
        self.entry_angle.insert(0, "12")
        self.entry_angle.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(content_frame, text="(5-30°)").grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Коэффициент сопротивления:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.drag_coefficient = ttk.Entry(content_frame, width=15)
        self.drag_coefficient.insert(0, "0.3")
        self.drag_coefficient.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Площадь сечения (м²):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.cross_section_area = ttk.Entry(content_frame, width=15)
        self.cross_section_area.insert(0, "1.5")
        self.cross_section_area.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Масса аппарата (кг):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mass_specified = ttk.Entry(content_frame, width=15)
        self.mass_specified.insert(0, "750")
        self.mass_specified.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Время симуляции (с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.simulation_time = ttk.Entry(content_frame, width=15)
        self.simulation_time.insert(0, "400")
        self.simulation_time.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Режим расчета массы:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mass_calculation_var = tk.StringVar(value="specified")
        ttk.Radiobutton(content_frame, text="Заданная масса", variable=self.mass_calculation_var, 
                       value="specified").grid(row=row, column=1, sticky=tk.W)
        ttk.Radiobutton(content_frame, text="Дирижабль", variable=self.mass_calculation_var,
                       value="airship").grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        ttk.Separator(content_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, 
                                                           sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Параметры дирижабля
        ttk.Label(content_frame, text="Параметры дирижабля:").grid(row=row, column=0, columnspan=3, 
                                                               sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Плотность оболочки (кг/м³):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.envelope_density = ttk.Entry(content_frame, width=15)
        self.envelope_density.insert(0, "0.8")
        self.envelope_density.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Масса полезной нагрузки (кг):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.payload_mass = ttk.Entry(content_frame, width=15)
        self.payload_mass.insert(0, "150")
        self.payload_mass.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Подъемная сила газа (кг/м³):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.gas_lift = ttk.Entry(content_frame, width=15)
        self.gas_lift.insert(0, "1.0")
        self.gas_lift.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Separator(content_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, 
                                                           sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Тепловые параметры
        ttk.Label(content_frame, text="Тепловые параметры:").grid(row=row, column=0, columnspan=3, 
                                                              sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Удельная теплоемкость (Дж/кг·K):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.specific_heat = ttk.Entry(content_frame, width=15)
        self.specific_heat.insert(0, "900")
        self.specific_heat.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Теплота плавления (Дж/кг):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.latent_heat = ttk.Entry(content_frame, width=15)
        self.latent_heat.insert(0, "20000000")
        self.latent_heat.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Температура плавления (K):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.melting_temp = ttk.Entry(content_frame, width=15)
        self.melting_temp.insert(0, "2100")
        self.melting_temp.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Макс. температура (K):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.max_temp = ttk.Entry(content_frame, width=15)
        self.max_temp.insert(0, "2300")
        self.max_temp.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Плотность материала (кг/м³):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.heat_shield_density = ttk.Entry(content_frame, width=15)
        self.heat_shield_density.insert(0, "600")
        self.heat_shield_density.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Толщина теплозащиты (м):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.heat_shield_thickness = ttk.Entry(content_frame, width=15)
        self.heat_shield_thickness.insert(0, "0.1")
        self.heat_shield_thickness.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Площадь теплозащиты (м²):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.heat_shield_area = ttk.Entry(content_frame, width=15)
        self.heat_shield_area.insert(0, "1.5")
        self.heat_shield_area.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Separator(content_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, 
                                                           sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Парашютная система
        ttk.Label(content_frame, text="Парашютная система:").grid(row=row, column=0, columnspan=3, 
                                                              sticky=tk.W, pady=5)
        row += 1
        
        self.use_parachutes_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(content_frame, text="Использовать парашюты", 
                       variable=self.use_parachutes_var).grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
        
        ttk.Label(content_frame, text="Площадь тормозного парашюта (м²):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.brake_chute_area = ttk.Entry(content_frame, width=15)
        self.brake_chute_area.insert(0, "4.0")
        self.brake_chute_area.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Скорость открытия тормозного (м/с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.brake_deploy_velocity = ttk.Entry(content_frame, width=15)
        self.brake_deploy_velocity.insert(0, "400")
        self.brake_deploy_velocity.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Площадь основного парашюта (м²):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.main_chute_area = ttk.Entry(content_frame, width=15)
        self.main_chute_area.insert(0, "40.0")
        self.main_chute_area.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Скорость открытия основного (м/с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.main_deploy_velocity = ttk.Entry(content_frame, width=15)
        self.main_deploy_velocity.insert(0, "50")
        self.main_deploy_velocity.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(content_frame, text="Скорость отстрела тормозного (м/с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.brake_jettison_velocity = ttk.Entry(content_frame, width=15)
        self.brake_jettison_velocity.insert(0, "50")
        self.brake_jettison_velocity.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Separator(content_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, 
                                                           sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Прогресс и кнопки
        self.progress = ttk.Progressbar(content_frame, length=300, mode='determinate')
        self.progress.grid(row=row, column=0, columnspan=3, pady=10)
        row += 1
        
        self.status_label = ttk.Label(content_frame, text="Готов к симуляции")
        self.status_label.grid(row=row, column=0, columnspan=3, pady=5)
        row += 1
        
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        self.run_button = ttk.Button(button_frame, text="Запустить симуляцию", 
                                    command=self.run_simulation, width=20)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Выход", command=self.root.quit, width=20).pack(side=tk.LEFT, padx=5)
        
        # Убедитесь, что колонки расширяются
        content_frame.columnconfigure(1, weight=1)
    
    def run_simulation(self):
        if self.running:
            return
        
        try:
            input_data = self._get_input_data()
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Некорректные данные: {e}")
            return
        
        self.running = True
        self.run_button.config(state='disabled')
        self.progress['value'] = 0
        self.status_label.config(text="Запуск симуляции...")
        
        thread = threading.Thread(target=self._run_simulation_thread, args=(input_data,))
        thread.daemon = True
        thread.start()
    
    def _get_input_data(self):
        thermal_props = ThermalProperties(
            specific_heat=float(self.specific_heat.get()),
            latent_heat=float(self.latent_heat.get()),
            melting_temperature=float(self.melting_temp.get()),
            max_temperature=float(self.max_temp.get()),
            density=float(self.heat_shield_density.get()),
            thickness=float(self.heat_shield_thickness.get()),
            area=float(self.heat_shield_area.get())
        )
        
        parachute_system = ParachuteSystem(
            use_parachutes=self.use_parachutes_var.get(),
            brake_chute_area=float(self.brake_chute_area.get()),
            main_chute_area=float(self.main_chute_area.get()),
            brake_deploy_velocity=float(self.brake_deploy_velocity.get()),
            main_deploy_velocity=float(self.main_deploy_velocity.get()),
            brake_jettison_velocity=float(self.brake_jettison_velocity.get())
        )
        
        input_data = SimulationInput(
            drag_coefficient=float(self.drag_coefficient.get()),
            cross_section_area=float(self.cross_section_area.get()),
            mass_specified=float(self.mass_specified.get()),
            entry_height=float(self.entry_height.get()) * 1000,
            entry_speed=float(self.entry_speed.get()),
            entry_angle=float(self.entry_angle.get()),
            simulation_time=float(self.simulation_time.get()),
            heat_shield_area=float(self.heat_shield_area.get()),
            thermal_properties=thermal_props,
            mass_calculation_mode=self.mass_calculation_var.get(),
            envelope_density=float(self.envelope_density.get()),
            payload_mass=float(self.payload_mass.get()),
            gas_lift=float(self.gas_lift.get()),
            parachute_system=parachute_system
        )
        
        return input_data
    
    def _run_simulation_thread(self, input_data):
        def progress_callback(progress, message):
            self.root.after(0, self._update_progress, progress, message)
        
        try:
            results = self.simulation_engine.run(input_data, progress_callback)
            self.root.after(0, self._show_results, results, input_data)
        except Exception as e:
            self.root.after(0, self._simulation_error, str(e))
    
    def _update_progress(self, progress, message):
        self.progress['value'] = progress
        self.status_label.config(text=message)
    
    def _show_results(self, results, input_data):
        self.running = False
        self.run_button.config(state='normal')
        self.status_label.config(text="Симуляция завершена")
        
        SimpleResultsWindow(self.root, results, input_data)
    
    def _simulation_error(self, error_message):
        self.running = False
        self.run_button.config(state='normal')
        self.status_label.config(text="Ошибка симуляции")
        messagebox.showerror("Ошибка симуляции", f"Произошла ошибка:\n{error_message}")