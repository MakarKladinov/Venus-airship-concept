import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
import numpy as np
from plots import (plot_speed_height, plot_heat_flux, plot_n_exponent, 
                  plot_trajectory, plot_temperatures,
                  plot_energy_balance,
                  plot_orbital_trajectory, plot_3d_trajectory,
                  plot_parachute_events)
from materials import plot_density_profile

class ResultsWindow:
    def __init__(self, parent, results, params, current_lang='ru'):
        self.results = results
        self.params = params
        self.current_lang = current_lang
        
        self.window = tk.Toplevel(parent)
        
        if current_lang == 'ru':
            self.window.title("Результаты моделирования")
        else:
            self.window.title("Simulation Results")
            
        self.window.geometry("1200x900")
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_summary_tab()
        self.create_entry_conditions_tab()
        self.create_parameters_tab()
        self.create_trajectory_tab()
        self.create_orbital_tab()
        self.create_heating_tab()
        self.create_airship_tab()
        self.create_parachute_tab()
        self.create_plots_tab()
    
    def create_summary_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Сводка")
        else:
            self.notebook.add(frame, text="Summary")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        summary = self.generate_summary_text()
        text_widget.insert(tk.END, summary)
        text_widget.config(state='disabled')
    
    def generate_summary_text(self):
        try:
            (C, A, m_specified, h0, v0_total, entry_angle, t_end, A_heat_shield, 
             c_solid, L, T_melt, T_max, T_initial, heat_shield_density, heat_shield_thickness,
             envelope_density, payload_mass, gas_lift_per_m3,
             mass_calculation_mode_int,
             use_parachute_int,
             brake_chute_area, brake_chute_coeff,
             brake_chute_deploy_velocity, main_chute_area,
             main_chute_coeff, brake_chute_jettison_velocity) = self.params
        except ValueError as e:
            if self.current_lang == 'ru':
                return f"ОШИБКА РАСПАКОВКИ ПАРАМЕТРОВ: {str(e)}\n"
            else:
                return f"PARAMETER UNPACKING ERROR: {str(e)}\n"
        
        mass_calculation_mode = bool(mass_calculation_mode_int)
        use_parachute = bool(use_parachute_int)
        initial_conditions = self.results.get('initial_conditions', {})
        airship_results = self.results.get('airship_results', {})
        parachute_events = self.results.get('parachute_events', {})
        
        import math
        R_nose = math.sqrt(A / math.pi) if A > 0 else 0
        
        if self.current_lang == 'ru':
            summary = f"""

                РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ ВХОДА В АТМОСФЕРУ ВЕНЕРЫ


НАЧАЛЬНЫЕ УСЛОВИЯ:

Угол входа:                  {entry_angle:>20.1f}° 
Скорость входа:              {v0_total:>20.0f} м/с
Высота входа:                {h0/1000:>20.1f} км
Радиус полусферы:            {R_nose:>20.2f} м
Режим расчета массы:         {'КАК ДИРИЖАБЛЬ' if mass_calculation_mode else 'ЗАДАННАЯ МАССА':>20}
Парашютная система:          {'ДА' if use_parachute else 'НЕТ':>20}
Шаг интегрирования:          {'0.001 с (1 мс) фиксированный':>20}

ОСНОВНЫЕ РЕЗУЛЬТАТЫ:


1. МАССА АППАРАТА:
   Режим расчета:            {'Дирижабль' if mass_calculation_mode else 'Заданная':>20}
"""
        else:
            summary = f"""

                VENUS ATMOSPHERIC ENTRY SIMULATION RESULTS


INITIAL CONDITIONS:

Entry angle:                  {entry_angle:>20.1f}° 
Entry speed:                 {v0_total:>20.0f} m/s
Entry height:                {h0/1000:>20.1f} km
Nose radius:                 {R_nose:>20.2f} m
Mass calculation mode:       {'AS AIRSHIP' if mass_calculation_mode else 'SPECIFIED MASS':>20}
Parachute system:            {'YES' if use_parachute else 'NO':>20}
Integration step:            {'0.001 s (1 ms) fixed':>20}

MAIN RESULTS:


1. VEHICLE MASS:
   Calculation mode:         {'Airship' if mass_calculation_mode else 'Specified':>20}
"""
        
        if mass_calculation_mode:
            if self.current_lang == 'ru':
                summary += f"""   Расчетная масса:          {airship_results.get('total_mass', 0):12.1f} кг
   Объем дирижабля:          {airship_results.get('volume', 0):12.1f} м³
   Радиус сферы:             {airship_results.get('radius', 0):12.2f} м
   Масса оболочки:           {airship_results.get('envelope_mass', 0):12.1f} кг
   Полезная нагрузка:        {airship_results.get('payload_mass', 0):12.1f} кг
"""
            else:
                summary += f"""   Calculated mass:          {airship_results.get('total_mass', 0):12.1f} kg
   Airship volume:           {airship_results.get('volume', 0):12.1f} m³
   Sphere radius:            {airship_results.get('radius', 0):12.2f} m
   Envelope mass:            {airship_results.get('envelope_mass', 0):12.1f} kg
   Payload mass:             {airship_results.get('payload_mass', 0):12.1f} kg
"""
        else:
            if self.current_lang == 'ru':
                summary += f"""   Заданная масса:           {m_specified:12.1f} кг
"""
            else:
                summary += f"""   Specified mass:           {m_specified:12.1f} kg
"""
        
        if self.current_lang == 'ru':
            summary += f"""
2. ТРАЕКТОРИЯ:
   Дальность полета:         {self.results.get('distance', 0)/1000:12.1f} км
   Время полета:             {self.results.get('impact_time', 0):12.1f} с
   Конечная скорость:        {self.results.get('final_velocity', 0):12.1f} м/с

3. ОРБИТАЛЬНЫЕ ПАРАМЕТРЫ:
   Угловое смещение:         {np.degrees(self.results.get('angular_displacement', 0)):12.1f}°
   Длина дуги траектории:    {self.results.get('arc_distance', 0)/1000:12.1f} км

4. ТЕПЛОВЫЕ НАГРУЗКИ:
   Макс. тепловой поток:     {self.results.get('max_heat_flux', 0)/1e6:12.2f} МВт/м²
   Конечная температура:     {self.results.get('surface_temp_final', 0):12.0f} K
   Полная тепловая энергия:  {self.results.get('total_heat', 0)/1e6:12.1f} МДж
"""
        else:
            summary += f"""
2. TRAJECTORY:
   Flight range:             {self.results.get('distance', 0)/1000:12.1f} km
   Flight time:              {self.results.get('impact_time', 0):12.1f} s
   Final velocity:           {self.results.get('final_velocity', 0):12.1f} m/s

3. ORBITAL PARAMETERS:
   Angular displacement:     {np.degrees(self.results.get('angular_displacement', 0)):12.1f}°
   Arc trajectory length:    {self.results.get('arc_distance', 0)/1000:12.1f} km

4. THERMAL LOADS:
   Max heat flux:            {self.results.get('max_heat_flux', 0)/1e6:12.2f} MW/m²
   Final temperature:        {self.results.get('surface_temp_final', 0):12.0f} K
   Total thermal energy:     {self.results.get('total_heat', 0)/1e6:12.1f} MJ
"""
        
        if use_parachute:
            if self.current_lang == 'ru':
                summary += f"""
5. ПАРАШЮТНАЯ СИСТЕМА:
   Тормозной парашют:        {brake_chute_area:12.1f} м²
   Основной парашют:         {main_chute_area:12.1f} м²
"""
            else:
                summary += f"""
5. PARACHUTE SYSTEM:
   Brake parachute:          {brake_chute_area:12.1f} m²
   Main parachute:           {main_chute_area:12.1f} m²
"""
            
            if parachute_events:
                if 'brake_deploy_time' in parachute_events:
                    t = parachute_events['brake_deploy_time']
                    v = parachute_events['brake_deploy_velocity']
                    h = parachute_events['brake_deploy_height']/1000
                    if self.current_lang == 'ru':
                        summary += f"   Тормозной открыт:        t={t:8.1f} с, v={v:.0f} м/с, h={h:.1f} км\n"
                    else:
                        summary += f"   Brake deployed:          t={t:8.1f} s, v={v:.0f} m/s, h={h:.1f} km\n"
                
                if 'main_deploy_time' in parachute_events:
                    t = parachute_events['main_deploy_time']
                    v = parachute_events['main_deploy_velocity']
                    h = parachute_events['main_deploy_height']/1000
                    if self.current_lang == 'ru':
                        summary += f"   Основной открыт:         t={t:8.1f} с, v={v:.0f} м/с, h={h:.1f} км\n"
                    else:
                        summary += f"   Main deployed:           t={t:8.1f} s, v={v:.0f} m/s, h={h:.1f} km\n"
                
                if 'brake_jettison_time' in parachute_events:
                    t = parachute_events['brake_jettison_time']
                    v = parachute_events['brake_jettison_velocity']
                    h = parachute_events['brake_jettison_height']/1000
                    if self.current_lang == 'ru':
                        summary += f"   Тормозной отстрелен:     t={t:8.1f} с, v={v:.0f} м/с, h={h:.1f} км\n"
                    else:
                        summary += f"   Brake jettisoned:        t={t:8.1f} s, v={v:.0f} m/s, h={h:.1f} km\n"
        
        summary += f"\n\n"
        
        return summary
    
    def create_entry_conditions_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Условия входа")
            frame_title = "Параметры входа в атмосферу"
        else:
            self.notebook.add(frame, text="Entry Conditions")
            frame_title = "Atmospheric Entry Parameters"
        
        entry_frame = ttk.LabelFrame(frame, text=frame_title, padding=10)
        entry_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        initial_conditions = self.results.get('initial_conditions', {})
        
        (C, A, m, h0, v0_total, entry_angle, t_end, A_heat_shield, 
         c_solid, L, T_melt, T_max, T_initial, heat_shield_density, heat_shield_thickness,
         envelope_density, payload_mass, gas_lift_per_m3,
         mass_calculation_mode_int,
         use_parachute_int,
         brake_chute_area, brake_chute_coeff,
         brake_chute_deploy_velocity, main_chute_area,
         main_chute_coeff, brake_chute_jettison_velocity) = self.params
        
        use_parachute = bool(use_parachute_int)
        
        import math
        R_nose = math.sqrt(A / math.pi) if A > 0 else 0
        
        vx0 = initial_conditions.get('vx0', 0)
        vy0 = initial_conditions.get('vy0', 0)
        
        if self.current_lang == 'ru':
            entry_text = f"""
        УСЛОВИЯ ВХОДА:
        
        Угол входа:                    {entry_angle:>20.1f}°
        Полная скорость входа:         {v0_total:>20.0f} м/с
        Высота входа:                  {h0/1000:>20.1f} км
        Площадь сечения:               {A:>20.2f} м²
        Расчетный радиус полусферы:    {R_nose:>20.2f} м
        Парашютная система:            {'ДА' if use_parachute else 'НЕТ':>20}
        
        РАСЧЕТНЫЕ КОМПОНЕНТЫ СКОРОСТИ:
        
        Горизонтальная скорость (vx):  {vx0:>20.0f} м/с
        Вертикальная скорость (vy):    {vy0:>20.0f} м/с
        Отношение vx/vy:               {vx0/vy0 if vy0 != 0 else float('inf'):>20.2f}
        
        АНАЛИЗ ТРАЕКТОРИИ:
        
        Горизонтальная дальность:      {self.results.get('distance', 0)/1000:>20.1f} км
        Время полета:                  {self.results.get('impact_time', 0):>20.1f} с
        Конечная скорость:             {self.results.get('final_velocity', 0):>20.1f} м/с
        
        ОРБИТАЛЬНЫЕ ПАРАМЕТРЫ:
        
        Угловое смещение:              {np.degrees(self.results.get('angular_displacement', 0)):>20.1f}°
        Длина дуги траектории:         {self.results.get('arc_distance', 0)/1000:>20.1f} км
        Конечная высота:               {self.results.get('final_height', 0):>20.1f} м
        """
        else:
            entry_text = f"""
        ENTRY CONDITIONS:
        
        Entry angle:                   {entry_angle:>20.1f}°
        Total entry speed:             {v0_total:>20.0f} m/s
        Entry height:                  {h0/1000:>20.1f} km
        Cross-section area:            {A:>20.2f} m²
        Calculated nose radius:        {R_nose:>20.2f} m
        Parachute system:              {'YES' if use_parachute else 'NO':>20}
        
        CALCULATED VELOCITY COMPONENTS:
        
        Horizontal velocity (vx):      {vx0:>20.0f} m/s
        Vertical velocity (vy):        {vy0:>20.0f} m/s
        Ratio vx/vy:                   {vx0/vy0 if vy0 != 0 else float('inf'):>20.2f}
        
        TRAJECTORY ANALYSIS:
        
        Horizontal range:              {self.results.get('distance', 0)/1000:>20.1f} km
        Flight time:                   {self.results.get('impact_time', 0):>20.1f} s
        Final velocity:                {self.results.get('final_velocity', 0):>20.1f} m/s
        
        ORBITAL PARAMETERS:
        
        Angular displacement:          {np.degrees(self.results.get('angular_displacement', 0)):>20.1f}°
        Arc trajectory length:         {self.results.get('arc_distance', 0)/1000:>20.1f} km
        Final height:                  {self.results.get('final_height', 0):>20.1f} m
        """
        
        text_widget = scrolledtext.ScrolledText(entry_frame, height=25, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, entry_text)
        text_widget.config(state='disabled')
    
    def create_parameters_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Параметры")
            frame_title = "Входные параметры"
        else:
            self.notebook.add(frame, text="Parameters")
            frame_title = "Input Parameters"
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        params_frame = ttk.LabelFrame(scrollable_frame, text=frame_title, padding=10)
        params_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        (C, A, m, h0, v0, entry_angle, t_end, A_heat_shield, 
         c_solid, L, T_melt, T_max, T_initial, heat_shield_density, heat_shield_thickness,
         envelope_density, payload_mass, gas_lift_per_m3,
         mass_calculation_mode_int,
         use_parachute_int,
         brake_chute_area, brake_chute_coeff,
         brake_chute_deploy_velocity, main_chute_area,
         main_chute_coeff, brake_chute_jettison_velocity) = self.params
        
        use_parachute = bool(use_parachute_int)
        mass_calculation_mode = bool(mass_calculation_mode_int)
        
        import math
        R_nose = math.sqrt(A / math.pi) if A > 0 else 0
        
        if self.current_lang == 'ru':
            params_text = f"""
        АЭРОДИНАМИЧЕСКИЕ ПАРАМЕТРЫ:
       
        Коэффициент сопротивления (C): {C}
        Площадь сечения (A): {A} м²
        Радиус полусферы (расчетный): {R_nose:.3f} м
        Масса аппарата (заданная): {m} кг
        
        НАЧАЛЬНЫЕ УСЛОВИЯ:
        
        Высота входа: {h0/1000:.1f} км
        Скорость входа: {v0} м/с ({abs(v0/1000):.1f} км/с)
        Угол входа: {entry_angle:.1f}°
        Время моделирования: {t_end} с
        
        ПАРАМЕТРЫ ИНТЕГРИРОВАНИЯ:
        
        Шаг интегрирования (dt): 0.001 с (фиксированный)
        
        ТЕПЛОЗАЩИТА:
        
        Площадь теплозащиты: {A_heat_shield} м²
        Толщина теплозащиты: {heat_shield_thickness} м
        
        СВОЙСТВА МАТЕРИАЛА ТЕПЛОЗАЩИТЫ:
        
        Удельная теплоемкость: {c_solid} Дж/(кг·K)
        Теплота плавления: {L/1e6:.1f} МДж/кг
        Температура плавления: {T_melt} K
        Макс. температура: {T_max} K
        Начальная температура: {T_initial} K
        Плотность теплозащиты: {heat_shield_density} кг/м³
        """
        else:
            params_text = f"""
        AERODYNAMIC PARAMETERS:
       
        Drag coefficient (C): {C}
        Cross-section area (A): {A} m²
        Nose radius (calculated): {R_nose:.3f} m
        Vehicle mass (specified): {m} kg
        
        INITIAL CONDITIONS:
        
        Entry height: {h0/1000:.1f} km
        Entry speed: {v0} m/s ({abs(v0/1000):.1f} km/s)
        Entry angle: {entry_angle:.1f}°
        Simulation time: {t_end} s
        
        INTEGRATION PARAMETERS:
        
        Integration step (dt): 0.001 s (fixed)
        
        HEAT SHIELD:
        
        Heat shield area: {A_heat_shield} m²
        Heat shield thickness: {heat_shield_thickness} m
        
        HEAT SHIELD MATERIAL PROPERTIES:
        
        Specific heat capacity: {c_solid} J/(kg·K)
        Latent heat of fusion: {L/1e6:.1f} MJ/kg
        Melting temperature: {T_melt} K
        Max temperature: {T_max} K
        Initial temperature: {T_initial} K
        Heat shield density: {heat_shield_density} kg/m³
        """
        
        if mass_calculation_mode:
            if self.current_lang == 'ru':
                params_text += f"""
        РЕЖИМ РАСЧЕТА МАССЫ:
        
        Режим: Расчет как дирижабль
        
        ПАРАМЕТРЫ ДИРИЖАБЛЯ:
        
        Плотность оболочки: {envelope_density} кг/м³
        Полезная нагрузка: {payload_mass} кг
        Подъемная сила газа: {gas_lift_per_m3} кг/м³
        """
            else:
                params_text += f"""
        MASS CALCULATION MODE:
        
        Mode: Calculate as airship
        
        AIRSHIP PARAMETERS:
        
        Envelope density: {envelope_density} kg/m³
        Payload mass: {payload_mass} kg
        Gas lift per m³: {gas_lift_per_m3} kg/m³
        """
        else:
            if self.current_lang == 'ru':
                params_text += f"""
        РЕЖИМ РАСЧЕТА МАССЫ:
        
        Режим: Заданная масса
        
        ПАРАМЕТРЫ ДИРИЖАБЛЯ:
        
        Не используются (режим заданной массы)
        """
            else:
                params_text += f"""
        MASS CALCULATION MODE:
        
        Mode: Specified mass
        
        AIRSHIP PARAMETERS:
        
        Not used (specified mass mode)
        """
        
        if use_parachute:
            if self.current_lang == 'ru':
                params_text += f"""
        
        ПАРАМЕТРЫ ПАРАШЮТНОЙ СИСТЕМЫ:
        
        Использование парашютов: ДА
        
        ТОРМОЗНОЙ ПАРАШЮТ:
        Площадь: {brake_chute_area} м²
        Коэффициент сопротивления: {brake_chute_coeff}
        Скорость открытия: {brake_chute_deploy_velocity} м/с
        Скорость отстрела: {brake_chute_jettison_velocity} м/с
        
        ОСНОВНОЙ ПАРАШЮТ:
        Площадь: {main_chute_area} м²
        Коэффициент сопротивления: {main_chute_coeff}
        Скорость открытия: {brake_chute_jettison_velocity} м/с (такая же как отстрел тормозного)
        """
            else:
                params_text += f"""
        
        PARACHUTE SYSTEM PARAMETERS:
        
        Use parachutes: YES
        
        BRAKE PARACHUTE:
        Area: {brake_chute_area} m²
        Drag coefficient: {brake_chute_coeff}
        Deployment velocity: {brake_chute_deploy_velocity} m/s
        Jettison velocity: {brake_chute_jettison_velocity} m/s
        
        MAIN PARACHUTE:
        Area: {main_chute_area} m²
        Drag coefficient: {main_chute_coeff}
        Deployment velocity: {brake_chute_jettison_velocity} m/s (same as brake jettison)
        """
        else:
            if self.current_lang == 'ru':
                params_text += f"""
        
        ПАРАМЕТРЫ ПАРАШЮТНОЙ СИСТЕМЫ:
        
        Использование парашютов: НЕТ
        """
            else:
                params_text += f"""
        
        PARACHUTE SYSTEM PARAMETERS:
        
        Use parachutes: NO
        """
        
        text_widget = tk.Text(params_frame, height=30, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, params_text)
        text_widget.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_trajectory_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Траектория")
            frame_title = "Результаты траектории"
        else:
            self.notebook.add(frame, text="Trajectory")
            frame_title = "Trajectory Results"
        
        traj_frame = ttk.LabelFrame(frame, text=frame_title, padding=10)
        traj_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        initial_conditions = self.results.get('initial_conditions', {})
        vx0 = initial_conditions.get('vx0', 0)
        vy0 = initial_conditions.get('vy0', 0)
        
        if self.current_lang == 'ru':
            traj_text = f"""
        КИНЕМАТИЧЕСКИЕ ПАРАМЕТРЫ:
        
        Дальность полета:               {self.results.get('distance', 0)/1000:8.1f} км
        Время полета:                   {self.results.get('impact_time', 0):8.1f} с
        Конечная высота:                {self.results.get('final_height', 0):8.1f} м
        
        СКОРОСТИ:
        
        Начальная горизонтальная (vx):  {vx0:8.0f} м/с
        Начальная вертикальная (vy):    {vy0:8.0f} м/с
        Начальная полная скорость:      {self.params[4]:8.0f} м/с
        Конечная скорость:              {self.results.get('final_velocity', 0):8.1f} м/с
        Торможение:                     {((abs(self.params[4]) - self.results.get('final_velocity', 0))/abs(self.params[4])*100) if self.params[4] != 0 else 0:8.1f} %
        
        АНАЛИЗ УГЛА ВХОДА:
        
        Угол входа:                     {self.params[5]:8.1f}°
        Соотношение vx/vy:              {vx0/vy0 if vy0 != 0 else float('inf'):8.2f}
        Теоретическая дальность:        {vx0/vy0 * self.params[3]/1000 if vy0 != 0 else 0:8.1f} км
        """
        else:
            traj_text = f"""
        KINEMATIC PARAMETERS:
        
        Flight range:                   {self.results.get('distance', 0)/1000:8.1f} km
        Flight time:                    {self.results.get('impact_time', 0):8.1f} s
        Final height:                   {self.results.get('final_height', 0):8.1f} m
        
        VELOCITIES:
        
        Initial horizontal (vx):        {vx0:8.0f} m/s
        Initial vertical (vy):          {vy0:8.0f} m/s
        Initial total speed:            {self.params[4]:8.0f} m/s
        Final velocity:                 {self.results.get('final_velocity', 0):8.1f} m/s
        Deceleration:                   {((abs(self.params[4]) - self.results.get('final_velocity', 0))/abs(self.params[4])*100) if self.params[4] != 0 else 0:8.1f} %
        
        ENTRY ANGLE ANALYSIS:
        
        Entry angle:                    {self.params[5]:8.1f}°
        Ratio vx/vy:                    {vx0/vy0 if vy0 != 0 else float('inf'):8.2f}
        Theoretical range:              {vx0/vy0 * self.params[3]/1000 if vy0 != 0 else 0:8.1f} km
        """
        
        text_widget = scrolledtext.ScrolledText(traj_frame, height=20, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, traj_text)
        text_widget.config(state='disabled')
    
    def create_orbital_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Орбитальные параметры")
            frame_title = "Орбитальные параметры траектории"
        else:
            self.notebook.add(frame, text="Orbital Parameters")
            frame_title = "Orbital Trajectory Parameters"
        
        orbital_frame = ttk.LabelFrame(frame, text=frame_title, padding=10)
        orbital_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        angular_displacement = np.degrees(self.results.get('angular_displacement', 0))
        arc_distance = self.results.get('arc_distance', 0) / 1000
        
        if self.current_lang == 'ru':
            orbital_text = f"""
        ОРБИТАЛЬНЫЕ ПАРАМЕТРЫ:
        
        Угловое смещение:               {angular_displacement:8.1f}°
        Длина дуги траектории:          {arc_distance:8.1f} км
        Начальный радиус орбиты:        {(6051800 + self.params[3])/1000:8.1f} км
        Конечный радиус орбита:         {(6051800 + self.results.get('final_height', 0))/1000:8.1f} км
        
        КООРДИНАТЫ:
        
        Начальная долгота:              0.0°
        Конечная долгота:               {self.results.get('lon', [0])[-1] if len(self.results.get('lon', [])) > 0 else 0:8.1f}°
        
        СКОРОСТИ В СФЕРИЧЕСКИХ КООРДИНАТАХ:
        
        Начальная азимутальная скорость: {self.results.get('v_theta', [0])[0] if len(self.results.get('v_theta', [])) > 0 else 0:8.1f} м/с
        Конечная азимутальная скорость:  {self.results.get('v_theta', [0])[-1] if len(self.results.get('v_theta', [])) > 0 else 0:8.1f} м/с
        Начальная радиальная скорость:   {self.results.get('v_r', [0])[0] if len(self.results.get('v_r', [])) > 0 else 0:8.1f} м/с
        Конечная радиальная скорость:    {self.results.get('v_r', [0])[-1] if len(self.results.get('v_r', [])) > 0 else 0:8.1f} м/с
        
        АНАЛИЗ ТРАЕКТОРИИ:
        
        Тип траектории:                 {'Спуск с орбиты' if self.params[3] > 100000 else 'Баллистический спуск'}
        Высота входа:                   {self.params[3]/1000:8.1f} км
        Угол входа:                     {self.params[5]:8.1f}°
        """
        else:
            orbital_text = f"""
        ORBITAL PARAMETERS:
        
        Angular displacement:           {angular_displacement:8.1f}°
        Arc trajectory length:          {arc_distance:8.1f} km
        Initial orbital radius:         {(6051800 + self.params[3])/1000:8.1f} km
        Final orbital radius:           {(6051800 + self.results.get('final_height', 0))/1000:8.1f} km
        
        COORDINATES:
        
        Initial longitude:              0.0°
        Final longitude:                {self.results.get('lon', [0])[-1] if len(self.results.get('lon', [])) > 0 else 0:8.1f}°
        
        SPHERICAL COORDINATE VELOCITIES:
        
        Initial azimuthal speed:        {self.results.get('v_theta', [0])[0] if len(self.results.get('v_theta', [])) > 0 else 0:8.1f} m/s
        Final azimuthal speed:          {self.results.get('v_theta', [0])[-1] if len(self.results.get('v_theta', [])) > 0 else 0:8.1f} m/s
        Initial radial speed:           {self.results.get('v_r', [0])[0] if len(self.results.get('v_r', [])) > 0 else 0:8.1f} m/s
        Final radial speed:             {self.results.get('v_r', [0])[-1] if len(self.results.get('v_r', [])) > 0 else 0:8.1f} m/s
        
        TRAJECTORY ANALYSIS:
        
        Trajectory type:                {'Orbital descent' if self.params[3] > 100000 else 'Ballistic descent'}
        Entry height:                   {self.params[3]/1000:8.1f} km
        Entry angle:                    {self.params[5]:8.1f}°
        """
        
        text_widget = scrolledtext.ScrolledText(orbital_frame, height=25, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, orbital_text)
        text_widget.config(state='disabled')
    
    def create_heating_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Нагрев")
            frame_title = "Результаты теплового расчета"
        else:
            self.notebook.add(frame, text="Heating")
            frame_title = "Thermal Calculation Results"
        
        heat_frame = ttk.LabelFrame(frame, text=frame_title, padding=10)
        heat_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        material_props = self.results.get('material_props', {})
        
        if self.current_lang == 'ru':
            heat_text = f"""
        ТЕПЛОВЫЕ НАГРУЗКИ:
        
        Максимальный тепловой поток:    {self.results.get('max_heat_flux', 0)/1e6:8.2f} МВт/м²
        Полная тепловая энергия:        {self.results.get('total_heat', 0)/1e6:8.1f} МДж
        Энергия на единицу площади:     {self.results.get('heat_per_area', 0)/1e6:8.1f} МДж/м²
        
        ТЕМПЕРАТУРЫ:
        
        Начальная температура:          {material_props.get('T_initial', 20):8.0f} K
        Конечная температура:           {self.results.get('surface_temp_final', 0):8.0f} K
        Температура плавления:          {material_props.get('T_melt', 2100):8.0f} K
        Достигнуто плавление:           {'ДА' if self.results.get('melting_reached', False) else 'НЕТ':>8}
        
        ТЕПЛОЗАЩИТА:
        
        Масса теплозащиты:              {self.results.get('heat_shield_mass', 0):8.1f} кг
        
        ПЛАВЛЕНИЕ:
        
        Доля расплавленного мат.:       {self.results.get('melted_fraction', 0):8.1f} %
        Масса расплавленного мат.:      {self.results.get('melted_mass', 0):8.1f} кг
        
        ЭФФЕКТИВНОСТЬ:
        
        Тепловой КПД:                   {self.results.get('heat_shield_efficiency', 0):8.1f} %
        Энергоемкость системы:          {self.results.get('energy_capacity', 0)/1e6:8.1f} МДж
        """
        else:
            heat_text = f"""
        THERMAL LOADS:
        
        Maximum heat flux:              {self.results.get('max_heat_flux', 0)/1e6:8.2f} MW/m²
        Total thermal energy:           {self.results.get('total_heat', 0)/1e6:8.1f} MJ
        Energy per unit area:           {self.results.get('heat_per_area', 0)/1e6:8.1f} MJ/m²
        
        TEMPERATURES:
        
        Initial temperature:            {material_props.get('T_initial', 20):8.0f} K
        Final temperature:              {self.results.get('surface_temp_final', 0):8.0f} K
        Melting temperature:            {material_props.get('T_melt', 2100):8.0f} K
        Melting reached:                {'YES' if self.results.get('melting_reached', False) else 'NO':>8}
        
        HEAT SHIELD:
        
        Heat shield mass:               {self.results.get('heat_shield_mass', 0):8.1f} kg
        
        MELTING:
        
        Melted material fraction:       {self.results.get('melted_fraction', 0):8.1f} %
        Melted material mass:           {self.results.get('melted_mass', 0):8.1f} kg
        
        EFFICIENCY:
        
        Thermal efficiency:             {self.results.get('heat_shield_efficiency', 0):8.1f} %
        System energy capacity:         {self.results.get('energy_capacity', 0)/1e6:8.1f} MJ
        """
        
        text_widget = scrolledtext.ScrolledText(heat_frame, height=25, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, heat_text)
        text_widget.config(state='disabled')
    
    def create_airship_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Дирижабль")
            frame_title = "Расчет параметров дирижабля"
        else:
            self.notebook.add(frame, text="Airship")
            frame_title = "Airship Parameter Calculation"
        
        airship_frame = ttk.LabelFrame(frame, text=frame_title, padding=10)
        airship_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        airship_results = self.results.get('airship_results', {})
        
        if self.current_lang == 'ru':
            airship_text = f"""
        РАСЧЕТ МАССЫ АППАРАТА КАК ДИРИЖАБЛЯ:
        
        ВХОДНЫЕ ПАРАМЕТРЫ:
        
        Плотность оболочки:             {self.params[15]:8.1f} кг/м³
        Полезная нагрузка:              {self.params[16]:8.1f} кг
        Подъемная сила газа:            {self.params[17]:8.3f} кг/м³
        
        ГЕОМЕТРИЯ ДИРИЖАБЛЯ:
        
        Радиус сферы:                   {airship_results.get('radius', 0):8.2f} м
        Объем дирижабля:                {airship_results.get('volume', 0):8.1f} м³
        Площадь поверхности:            {airship_results.get('surface_area', 0):8.1f} м²
        
        РАСЧЕТ МАСС:
        
        Масса оболочки:                 {airship_results.get('envelope_mass', 0):8.1f} кг
        Полезная нагрузка:              {airship_results.get('payload_mass', 0):8.1f} кг
        Масса теплозащиты:              {airship_results.get('heat_shield_mass', 0):8.1f} кг
        Общая масса (без теплозащиты):  {airship_results.get('total_mass_for_lift', 0):8.1f} кг
        Полная масса (с теплозащитой):  {airship_results.get('total_mass', 0):8.1f} кг
        
        БАЛАНС ПОДЪЕМНЫХ СИЛ:
        
        Подъемная сила газа:            {airship_results.get('lift_force', 0)/1000:8.1f} кН
        Вес аппарата (без теплозащиты): {airship_results.get('weight_force', 0)/1000:8.1f} кН
        
        АНАЛИЗ РЕЗУЛЬТАТОВ:
        
        Массовая доля оболочки:         {(airship_results.get('envelope_mass', 0)/airship_results.get('total_mass', 1)*100) if airship_results.get('total_mass', 0) > 0 else 0:8.1f} %
        Массовая доля полезной нагрузки:{(airship_results.get('payload_mass', 0)/airship_results.get('total_mass', 1)*100) if airship_results.get('total_mass', 0) > 0 else 0:8.1f} %
        Массовая доля теплозащиты:      {(airship_results.get('heat_shield_mass', 0)/airship_results.get('total_mass', 1)*100) if airship_results.get('total_mass', 0) > 0 else 0:8.1f} %
        
        ПЛОТНОСТЬ КОНСТРУКЦИИ:
        
        Средняя плотность (без теплозащиты): {(airship_results.get('total_mass_for_lift', 0)/airship_results.get('volume', 1)) if airship_results.get('volume', 0) > 0 else 0:8.2f} кг/м³
        Средняя плотность (с теплозащитой):  {(airship_results.get('total_mass', 0)/airship_results.get('volume', 1)) if airship_results.get('volume', 0) > 0 else 0:8.2f} кг/м³
        """
        else:
            airship_text = f"""
        VEHICLE MASS CALCULATION AS AIRSHIP:
        
        INPUT PARAMETERS:
        
        Envelope density:               {self.params[15]:8.1f} kg/m³
        Payload mass:                   {self.params[16]:8.1f} kg
        Gas lift per m³:                {self.params[17]:8.3f} kg/m³
        
        AIRSHIP GEOMETRY:
        
        Sphere radius:                  {airship_results.get('radius', 0):8.2f} m
        Airship volume:                 {airship_results.get('volume', 0):8.1f} m³
        Surface area:                   {airship_results.get('surface_area', 0):8.1f} m²
        
        MASS CALCULATION:
        
        Envelope mass:                  {airship_results.get('envelope_mass', 0):8.1f} kg
        Payload mass:                   {airship_results.get('payload_mass', 0):8.1f} kg
        Heat shield mass:               {airship_results.get('heat_shield_mass', 0):8.1f} kg
        Total mass (without heat shield): {airship_results.get('total_mass_for_lift', 0):8.1f} kg
        Total mass (with heat shield):  {airship_results.get('total_mass', 0):8.1f} kg
        
        LIFT FORCE BALANCE:
        
        Gas lift force:                 {airship_results.get('lift_force', 0)/1000:8.1f} kN
        Vehicle weight (without heat shield): {airship_results.get('weight_force', 0)/1000:8.1f} kN
        
        RESULT ANALYSIS:
        
        Envelope mass fraction:         {(airship_results.get('envelope_mass', 0)/airship_results.get('total_mass', 1)*100) if airship_results.get('total_mass', 0) > 0 else 0:8.1f} %
        Payload mass fraction:          {(airship_results.get('payload_mass', 0)/airship_results.get('total_mass', 1)*100) if airship_results.get('total_mass', 0) > 0 else 0:8.1f} %
        Heat shield mass fraction:      {(airship_results.get('heat_shield_mass', 0)/airship_results.get('total_mass', 1)*100) if airship_results.get('total_mass', 0) > 0 else 0:8.1f} %
        
        STRUCTURE DENSITY:
        
        Average density (without heat shield): {(airship_results.get('total_mass_for_lift', 0)/airship_results.get('volume', 1)) if airship_results.get('volume', 0) > 0 else 0:8.2f} kg/m³
        Average density (with heat shield):  {(airship_results.get('total_mass', 0)/airship_results.get('volume', 1)) if airship_results.get('volume', 0) > 0 else 0:8.2f} kg/m³
        """
        
        text_widget = scrolledtext.ScrolledText(airship_frame, height=30, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, airship_text)
        text_widget.config(state='disabled')
    
    def create_parachute_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Парашюты")
            frame_title = "Результаты работы парашютной системы"
        else:
            self.notebook.add(frame, text="Parachutes")
            frame_title = "Parachute System Operation Results"
        
        parachute_frame = ttk.LabelFrame(frame, text=frame_title, padding=10)
        parachute_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        (C, A, m, h0, v0_total, entry_angle, t_end, A_heat_shield, 
         c_solid, L, T_melt, T_max, T_initial, heat_shield_density, heat_shield_thickness,
         envelope_density, payload_mass, gas_lift_per_m3,
         mass_calculation_mode_int,
         use_parachute_int,
         brake_chute_area, brake_chute_coeff,
         brake_chute_deploy_velocity, main_chute_area,
         main_chute_coeff, brake_chute_jettison_velocity) = self.params
        
        use_parachute = bool(use_parachute_int)
        parachute_events = self.results.get('parachute_events', {})
        brake_deployed = self.results.get('brake_chute_deployed', False)
        main_deployed = self.results.get('main_chute_deployed', False)
        brake_jettisoned = self.results.get('brake_chute_jettisoned', False)
        
        if self.current_lang == 'ru':
            parachute_text = f"""
        ПАРАМЕТРЫ ПАРАШЮТНОЙ СИСТЕМЫ:
        
        Использование парашютов:           {'ДА' if use_parachute else 'НЕТ'}
        
        ТОРМОЗНОЙ ПАРАШЮТ:
        
        Площадь:                          {brake_chute_area:8.1f} м²
        Коэффициент сопротивления:        {brake_chute_coeff:8.2f}
        Скорость открытия:                {brake_chute_deploy_velocity:8.0f} м/с
        Скорость отстрела:                {brake_chute_jettison_velocity:8.0f} м/с
        
        ОСНОВНОЙ ПАРАШЮТ:
        
        Площадь:                          {main_chute_area:8.1f} м²
        Коэффициент сопротивления:        {main_chute_coeff:8.2f}
        Скорость открытия:                {brake_chute_jettison_velocity:8.0f} м/с (такая же как отстрел тормозного)
        
        РЕЗУЛЬТАТЫ РАБОТЫ:
        
        Тормозной парашют открыт:         {'ДА' if brake_deployed else 'НЕТ'}
        Основной парашют открыт:          {'ДА' if main_deployed else 'НЕТ'}
        Тормозной парашют отстрелен:      {'ДА' if brake_jettisoned else 'НЕТ'}
        """
        else:
            parachute_text = f"""
        PARACHUTE SYSTEM PARAMETERS:
        
        Use parachutes:                   {'YES' if use_parachute else 'NO'}
        
        BRAKE PARACHUTE:
        
        Area:                            {brake_chute_area:8.1f} m²
        Drag coefficient:                {brake_chute_coeff:8.2f}
        Deployment velocity:             {brake_chute_deploy_velocity:8.0f} m/s
        Jettison velocity:               {brake_chute_jettison_velocity:8.0f} m/s
        
        MAIN PARACHUTE:
        
        Area:                            {main_chute_area:8.1f} m²
        Drag coefficient:                {main_chute_coeff:8.2f}
        Deployment velocity:             {brake_chute_jettison_velocity:8.0f} m/s (same as brake jettison)
        
        OPERATION RESULTS:
        
        Brake parachute deployed:        {'YES' if brake_deployed else 'NO'}
        Main parachute deployed:         {'YES' if main_deployed else 'NO'}
        Brake parachute jettisoned:      {'YES' if brake_jettisoned else 'NO'}
        """
        
        if parachute_events:
            if self.current_lang == 'ru':
                parachute_text += f"""
        
        СОБЫТИЯ ПАРАШЮТОВ:
        
        """
            else:
                parachute_text += f"""
        
        PARACHUTE EVENTS:
        
        """
                
            if 'brake_deploy_time' in parachute_events:
                t = parachute_events['brake_deploy_time']
                v = parachute_events['brake_deploy_velocity']
                h = parachute_events['brake_deploy_height']
                if self.current_lang == 'ru':
                    parachute_text += f"Тормозной открыт:           t={t:8.1f} с, v={v:8.0f} м/с\n"
                else:
                    parachute_text += f"Brake deployed:            t={t:8.1f} s, v={v:8.0f} m/s\n"
            
            if 'main_deploy_time' in parachute_events:
                t = parachute_events['main_deploy_time']
                v = parachute_events['main_deploy_velocity']
                h = parachute_events['main_deploy_height']
                if self.current_lang == 'ru':
                    parachute_text += f"	Основной открыт:            t={t:8.1f} с, v={v:8.0f} м/с\n"
                else:
                    parachute_text += f"	Main deployed:              t={t:8.1f} s, v={v:8.0f} m/s\n"
            
            if 'brake_jettison_time' in parachute_events:
                t = parachute_events['brake_jettison_time']
                v = parachute_events['brake_jettison_velocity']
                h = parachute_events['brake_jettison_height']
                if self.current_lang == 'ru':
                    parachute_text += f"	Тормозной отстрелен:        t={t:8.1f} с, v={v:8.0f} м/с\n"
                else:
                    parachute_text += f"	Brake jettisoned:           t={t:8.1f} s, v={v:8.0f} m/s\n"
        
        if use_parachute and len(self.results.get('time', [])) > 0:
            time = self.results['time']
            v_total = self.results['v_total']
            
            if 'parachute_state' in self.results:
                states = self.results['parachute_state']
                time_without_parachute = 0
                time_with_parachute = 0
                
                for i in range(len(states) - 1):
                    dt = time[i+1] - time[i]
                    if states[i] == 'none':
                        time_without_parachute += dt
                    else:
                        time_with_parachute += dt
                
                if self.current_lang == 'ru':
                    parachute_text += f"""
        
        АНАЛИЗ ЭФФЕКТИВНОСТИ:
        
        Время без парашютов:              {time_without_parachute:8.1f} с
        Время с парашютами:               {time_with_parachute:8.1f} с
        Отношение времени:                {time_with_parachute/time_without_parachute if time_without_parachute > 0 else 0:8.2f}
        
        СКОРОСТИ:
        
        Начальная скорость:               {self.results['initial_conditions']['v0_total']:8.0f} м/с
        Скорость при открытии тормозного: {parachute_events.get('brake_deploy_velocity', 0):8.0f} м/с
        Скорость при открытии основного:  {parachute_events.get('main_deploy_velocity', 0):8.0f} м/с
        Конечная скорость:                {self.results.get('final_velocity', 0):8.1f} м/с
        """
                else:
                    parachute_text += f"""
        
        EFFICIENCY ANALYSIS:
        
        Time without parachutes:          {time_without_parachute:8.1f} s
        Time with parachutes:             {time_with_parachute:8.1f} s
        Time ratio:                       {time_with_parachute/time_without_parachute if time_without_parachute > 0 else 0:8.2f}
        
        VELOCITIES:
        
        Initial speed:                    {self.results['initial_conditions']['v0_total']:8.0f} m/s
        Speed at brake deployment:        {parachute_events.get('brake_deploy_velocity', 0):8.0f} m/s
        Speed at main deployment:         {parachute_events.get('main_deploy_velocity', 0):8.0f} m/s
        Final velocity:                   {self.results.get('final_velocity', 0):8.1f} m/s
        """
            
            if 'initial_conditions' in self.results:
                v0 = self.results['initial_conditions']['v0_total']
                v_final = self.results.get('final_velocity', 0)
                braking_efficiency = ((v0 - v_final) / v0 * 100) if v0 > 0 else 0
                
                if self.current_lang == 'ru':
                    parachute_text += f"""
        
        ЭФФЕКТИВНОСТЬ ТОРМОЖЕНИЯ:
        
        Снижение скорости:                {v0 - v_final:8.0f} м/с
        Процент снижения:                 {braking_efficiency:8.1f} %
        Ускорение торможения (ср.):       {(v0 - v_final)/time[-1] if time[-1] > 0 else 0:8.2f} м/с²
                """
                else:
                    parachute_text += f"""
        
        BRAKING EFFICIENCY:
        
        Speed reduction:                  {v0 - v_final:8.0f} m/s
        Percentage reduction:             {braking_efficiency:8.1f} %
        Average braking acceleration:     {(v0 - v_final)/time[-1] if time[-1] > 0 else 0:8.2f} m/s²
                """
        
        text_widget = scrolledtext.ScrolledText(parachute_frame, height=30, font=("Courier", 9))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(tk.END, parachute_text)
        text_widget.config(state='disabled')
    
    def create_plots_tab(self):
        frame = ttk.Frame(self.notebook)
        
        if self.current_lang == 'ru':
            self.notebook.add(frame, text="Графики")
            frame_title = "Графики результатов"
            categories = [
                ("ОСНОВНЫЕ ГРАФИКИ", [
                    ("Скорость и высота", 'speed_height'),
                    ("Тепловой поток", 'heat'),
                    ("Траектория", 'trajectory'),
                ]),
                ("ОРБИТАЛЬНЫЕ ГРАФИКИ", [
                    ("Орбитальные параметры", 'orbital'),
                    ("3D траектория", '3d_trajectory'),
                ]),
                ("ТЕПЛОВЫЕ ГРАФИКИ", [
                    ("Температуры", 'temperatures'),
                    ("Баланс энергий", 'energy_balance'),
                    ("Показатель n(v)", 'n_exponent'),
                ]),
                ("ПАРАШЮТЫ", [
                    ("Открытие парашютов", 'parachute_events'),
                ]),
                ("АТМОСФЕРА", [
                    ("Плотность атмосферы", 'density'),
                ])
            ]
            info_text = """
        Для построения графика нажмите соответствующую кнопку.
        Графики откроются в отдельных окнах.
        Закройте окно графика для возврата к программе.
        """
        else:
            self.notebook.add(frame, text="Plots")
            frame_title = "Result Plots"
            categories = [
                ("MAIN PLOTS", [
                    ("Speed and Height", 'speed_height'),
                    ("Heat Flux", 'heat'),
                    ("Trajectory", 'trajectory'),
                ]),
                ("ORBITAL PLOTS", [
                    ("Orbital Parameters", 'orbital'),
                    ("3D Trajectory", '3d_trajectory'),
                ]),
                ("THERMAL PLOTS", [
                    ("Temperatures", 'temperatures'),
                    ("Energy Balance", 'energy_balance'),
                    ("n(v) Exponent", 'n_exponent'),
                ]),
                ("PARACHUTES", [
                    ("Parachute Events", 'parachute_events'),
                ]),
                ("ATMOSPHERE", [
                    ("Density Profile", 'density'),
                ])
            ]
            info_text = """
        Click the corresponding button to plot.
        Plots will open in separate windows.
        Close the plot window to return to the program.
        """
        
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        plots_frame = ttk.LabelFrame(scrollable_frame, text=frame_title, padding=10)
        plots_frame.pack(fill='both', expand=True)
        
        btn_frame = ttk.Frame(plots_frame)
        btn_frame.pack(pady=10, fill='x')
        
        row_offset = 0
        for category_name, plots in categories:
            category_label = ttk.Label(btn_frame, text=category_name, 
                                      font=('TkDefaultFont', 10, 'bold'))
            category_label.grid(row=row_offset, column=0, columnspan=3, 
                               sticky='w', pady=(10, 5), padx=5)
            row_offset += 1
            
            for i, (text, plot_type) in enumerate(plots):
                row = row_offset + (i // 3)
                col = i % 3
                
                btn = ttk.Button(btn_frame, text=text, 
                               command=lambda pt=plot_type: self.show_plot(pt),
                               width=22)
                btn.grid(row=row, column=col, padx=5, pady=3, sticky='ew')
            
            row_offset += (len(plots) + 2) // 3
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        info_label = ttk.Label(plots_frame, text=info_text, justify='center')
        info_label.pack(pady=20)
    
    def show_plot(self, plot_type):
        try:
            if plot_type == 'speed_height':
                plot_speed_height(self.results)
            elif plot_type == 'heat':
                plot_heat_flux(self.results)
            elif plot_type == 'n_exponent':
                plot_n_exponent(self.results)
            elif plot_type == 'trajectory':
                plot_trajectory(self.results)
            elif plot_type == 'temperatures':
                plot_temperatures(self.results)
            elif plot_type == 'energy_balance':
                plot_energy_balance(self.results)
            elif plot_type == 'orbital':
                plot_orbital_trajectory(self.results)
            elif plot_type == '3d_trajectory':
                plot_3d_trajectory(self.results)
            elif plot_type == 'parachute_events':
                plot_parachute_events(self.results)
            elif plot_type == 'density':
                self.show_density_plot()
        except Exception as e:
            if self.current_lang == 'ru':
                messagebox.showerror("Ошибка построения графика", 
                                   f"Не удалось построить график:\n{str(e)}")
            else:
                messagebox.showerror("Plot Error", 
                                   f"Failed to plot:\n{str(e)}")
    
    def show_density_plot(self):
        try:
            fig = plot_density_profile(150000)
            plt.show()
        except Exception as e:
            if self.current_lang == 'ru':
                messagebox.showerror("Ошибка", f"Не удалось построить график плотности:\n{str(e)}")
            else:
                messagebox.showerror("Error", f"Failed to plot density profile:\n{str(e)}")