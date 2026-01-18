import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from simulation_engine import run_simulation
from results_window import ResultsWindow

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование входа в атмосферу Венеры")
        
        self.languages = {
            'ru': {
                'title': "Моделирование входа в атмосферу Венеры",
                'sim_params': "Параметры моделирования",
                'init_conditions': "Начальные условия",
                'mass_calc_mode': "Режим расчета массы аппарата",
                'parachute_system': "Парашютная система",
                'calc_vx_vy': "Рассчитать vx/vy",
                'horizontal_vel': "Гориз. скорость vx (м/с):",
                'vertical_vel': "Вертик. скорость vy (м/с):",
                'specified_mass': "Заданная масса",
                'airship_calc': "Расчет как дирижабль",
                'given_mass': "Заданная масса (кг):",
                'airship_params': "Параметры дирижабля:",
                'envelope_density': "Плотность оболочки (кг/м³):",
                'payload_mass': "Полезная нагрузка (кг):",
                'gas_lift': "Подъемная сила газа (кг/м³):",
                'use_parachute': "Использовать парашютную систему",
                'brake_parachute': "ТОРМОЗНОЙ ПАРАШЮТ",
                'main_parachute': "ОСНОВНОЙ ПАРАШЮТ",
                'area': "Площадь (м²):",
                'coeff_c': "Коэффициент C:",
                'deploy_vel': "Скорость открытия (м/с):",
                'jettison_vel': "Скорость отстрела (м/с):",
                'drag_coeff': "Коэффициент сопротивления:",
                'cross_section': "Площадь сечения (м²):",
                'sim_time': "Время моделирования (с):",
                'heat_shield_area': "Площадь теплозащиты (м²):",
                'specific_heat': "Удельная теплоемкость (Дж/(кг·K)):",
                'latent_heat': "Теплота плавления (Дж/кг):",
                'melt_temp': "Температура плавления (K):",
                'max_temp': "Макс. температура (K):",
                'init_temp': "Начальная температура (K):",
                'heat_shield_density': "Плотность теплозащиты (кг/м³):",
                'heat_shield_thickness': "Толщина теплозащиты (м):",
                'ready': "Готов к расчету",
                'run_sim': "Запустить моделирование",
                'default_params': "Параметры по умолчанию",
                'show_density': "Показать график плотности",
                'change_lang': "EN",
                'entry_height': "Высота входа (м):",
                'entry_speed': "Скорость входа (м/с):",
                'entry_angle': "Угол входа (град, 0-90):",
            },
            'en': {
                'title': "Venus Atmospheric Entry Simulation",
                'sim_params': "Simulation Parameters",
                'init_conditions': "Initial Conditions",
                'mass_calc_mode': "Vehicle Mass Calculation Mode",
                'parachute_system': "Parachute System",
                'calc_vx_vy': "Calculate vx/vy",
                'horizontal_vel': "Horizontal velocity vx (m/s):",
                'vertical_vel': "Vertical velocity vy (m/s):",
                'specified_mass': "Specified mass",
                'airship_calc': "Calculate as airship",
                'given_mass': "Specified mass (kg):",
                'airship_params': "Airship parameters:",
                'envelope_density': "Envelope density (kg/m³):",
                'payload_mass': "Payload mass (kg):",
                'gas_lift': "Gas lift per m³ (kg/m³):",
                'use_parachute': "Use parachute system",
                'brake_parachute': "BRAKE PARACHUTE",
                'main_parachute': "MAIN PARACHUTE",
                'area': "Area (m²):",
                'coeff_c': "Coefficient C:",
                'deploy_vel': "Deployment velocity (m/s):",
                'jettison_vel': "Jettison velocity (m/s):",
                'drag_coeff': "Drag coefficient:",
                'cross_section': "Cross-section area (m²):",
                'sim_time': "Simulation time (s):",
                'heat_shield_area': "Heat shield area (m²):",
                'specific_heat': "Specific heat capacity (J/(kg·K)):",
                'latent_heat': "Latent heat of fusion (J/kg):",
                'melt_temp': "Melting temperature (K):",
                'max_temp': "Max temperature (K):",
                'init_temp': "Initial temperature (K):",
                'heat_shield_density': "Heat shield density (kg/m³):",
                'heat_shield_thickness': "Heat shield thickness (m):",
                'ready': "Ready for calculation",
                'run_sim': "Run Simulation",
                'default_params': "Default Parameters",
                'show_density': "Show Density Plot",
                'change_lang': "RU",
                'entry_height': "Entry height (m):",
                'entry_speed': "Entry speed (m/s):",
                'entry_angle': "Entry angle (deg, 0-90):",
            }
        }
        
        self.current_lang = 'ru'
        
        self.default_params = {
            'C': 0.3,
            'A': 1.5,  
            'm': 750.0,
            'h0': 250000.0,  
            'v0': 7500.0,
            'entry_angle': 12.0, 
            't_end': 400.0,
            'A_heat_shield': 1.5,  
            'c_solid': 900.0,
            'L': 20e6,
            'T_melt': 2100.0,
            'T_max': 2300.0,
            'T_initial': 20.0,
            'heat_shield_density': 600.0,
            'heat_shield_thickness': 0.1,
            'envelope_density': 0.8,
            'payload_mass': 150.0,
            'gas_lift_per_m3': 1.0,
            'use_parachute': False,  
            'brake_chute_area': 4.0,  
            'main_chute_area': 40.0, 
            'brake_chute_coeff': 0.8,  
            'main_chute_coeff': 1.2, 
            'brake_chute_deploy_velocity': 400.0,  
            'brake_chute_jettison_velocity': 50.0,  
            'mass_calculation_mode': 'airship',
        }
        
        self.results_window = None
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
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
        
        input_frame = ttk.LabelFrame(scrollable_frame, text=self.languages[self.current_lang]['sim_params'], padding=10)
        input_frame.pack(fill='both', expand=True)
        
        self.entries = {}
        self.labels = {}  # Для хранения ссылок на метки для обновления языка
        row = 0
        
        init_frame = ttk.LabelFrame(input_frame, text=self.languages[self.current_lang]['init_conditions'], padding=5)
        init_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        init_row = 0
        
        # Высота входа
        label = ttk.Label(init_frame, text=self.languages[self.current_lang]['entry_height'])
        label.grid(row=init_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['entry_height'] = label
        
        entry = ttk.Entry(init_frame, width=15)
        entry.insert(0, str(self.default_params['h0']))
        entry.grid(row=init_row, column=1, padx=5, pady=2)
        self.entries['h0'] = entry
        init_row += 1
        
        # Скорость входа
        label = ttk.Label(init_frame, text=self.languages[self.current_lang]['entry_speed'])
        label.grid(row=init_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['entry_speed'] = label
        
        entry = ttk.Entry(init_frame, width=15)
        entry.insert(0, str(self.default_params['v0']))
        entry.grid(row=init_row, column=1, padx=5, pady=2)
        self.entries['v0'] = entry
        init_row += 1
        
        # Угол входа
        label = ttk.Label(init_frame, text=self.languages[self.current_lang]['entry_angle'])
        label.grid(row=init_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['entry_angle'] = label
        
        entry = ttk.Entry(init_frame, width=15)
        entry.insert(0, str(self.default_params['entry_angle']))
        entry.grid(row=init_row, column=1, padx=5, pady=2)
        self.entries['entry_angle'] = entry
        
        calc_btn = ttk.Button(init_frame, text=self.languages[self.current_lang]['calc_vx_vy'], 
                            command=self.calculate_velocity_components)
        calc_btn.grid(row=init_row, column=2, padx=10, pady=2)
        self.labels['calc_vx_vy'] = calc_btn
        init_row += 1
        
        # Горизонтальная скорость
        label = ttk.Label(init_frame, text=self.languages[self.current_lang]['horizontal_vel'])
        label.grid(row=init_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['horizontal_vel'] = label
        
        vx_entry = ttk.Entry(init_frame, width=15, state='readonly')
        vx_entry.grid(row=init_row, column=1, padx=5, pady=2)
        self.vx_display = vx_entry
        init_row += 1
        
        # Вертикальная скорость
        label = ttk.Label(init_frame, text=self.languages[self.current_lang]['vertical_vel'])
        label.grid(row=init_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['vertical_vel'] = label
        
        vy_entry = ttk.Entry(init_frame, width=15, state='readonly')
        vy_entry.grid(row=init_row, column=1, padx=5, pady=2)
        self.vy_display = vy_entry
        init_row += 1
        
        row += 1
        
        # Режим расчета массы
        mass_frame = ttk.LabelFrame(input_frame, text=self.languages[self.current_lang]['mass_calc_mode'], padding=5)
        mass_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        mass_row = 0
        
        self.mass_mode_var = tk.StringVar(value=self.default_params['mass_calculation_mode'])
        
        rb1 = ttk.Radiobutton(mass_frame, text=self.languages[self.current_lang]['specified_mass'], 
                       variable=self.mass_mode_var, value='specified',
                       command=self.toggle_mass_fields)
        rb1.grid(row=mass_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['specified_mass'] = rb1
        
        rb2 = ttk.Radiobutton(mass_frame, text=self.languages[self.current_lang]['airship_calc'], 
                       variable=self.mass_mode_var, value='airship',
                       command=self.toggle_mass_fields)
        rb2.grid(row=mass_row, column=1, sticky="w", padx=5, pady=2)
        self.labels['airship_calc'] = rb2
        mass_row += 1
        
        # Заданная масса
        label = ttk.Label(mass_frame, text=self.languages[self.current_lang]['given_mass'])
        label.grid(row=mass_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['given_mass'] = label
        
        entry = ttk.Entry(mass_frame, width=15)
        entry.insert(0, str(self.default_params['m']))
        entry.grid(row=mass_row, column=1, padx=5, pady=2)
        self.entries['m'] = entry
        mass_row += 1
        
        # Параметры дирижабля
        label = ttk.Label(mass_frame, text=self.languages[self.current_lang]['airship_params'], font=('TkDefaultFont', 9, 'bold'))
        label.grid(row=mass_row, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        self.labels['airship_params'] = label
        mass_row += 1
        
        # Плотность оболочки
        label = ttk.Label(mass_frame, text=self.languages[self.current_lang]['envelope_density'])
        label.grid(row=mass_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['envelope_density'] = label
        
        entry = ttk.Entry(mass_frame, width=15)
        entry.insert(0, str(self.default_params['envelope_density']))
        entry.grid(row=mass_row, column=1, padx=5, pady=2)
        self.entries['envelope_density'] = entry
        mass_row += 1
        
        # Полезная нагрузка
        label = ttk.Label(mass_frame, text=self.languages[self.current_lang]['payload_mass'])
        label.grid(row=mass_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['payload_mass'] = label
        
        entry = ttk.Entry(mass_frame, width=15)
        entry.insert(0, str(self.default_params['payload_mass']))
        entry.grid(row=mass_row, column=1, padx=5, pady=2)
        self.entries['payload_mass'] = entry
        mass_row += 1
        
        # Подъемная сила газа
        label = ttk.Label(mass_frame, text=self.languages[self.current_lang]['gas_lift'])
        label.grid(row=mass_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['gas_lift'] = label
        
        entry = ttk.Entry(mass_frame, width=15)
        entry.insert(0, str(self.default_params['gas_lift_per_m3']))
        entry.grid(row=mass_row, column=1, padx=5, pady=2)
        self.entries['gas_lift_per_m3'] = entry
        mass_row += 1
        
        row += 1
        
        # Парашютная система
        chute_frame = ttk.LabelFrame(input_frame, text=self.languages[self.current_lang]['parachute_system'], padding=5)
        chute_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        chute_row = 0

        self.use_parachute_var = tk.BooleanVar(value=self.default_params['use_parachute'])
        cb = ttk.Checkbutton(chute_frame, text=self.languages[self.current_lang]['use_parachute'], 
                       variable=self.use_parachute_var,
                       command=self.toggle_parachute_fields)
        cb.grid(row=chute_row, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        self.labels['use_parachute'] = cb
        chute_row += 1

        # Тормозной парашют
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['brake_parachute'], font=('TkDefaultFont', 9, 'bold'))
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=5)
        self.labels['brake_parachute'] = label
        chute_row += 1
        
        # Площадь тормозного парашюта
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['area'])
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['area'] = label
        
        entry = ttk.Entry(chute_frame, width=15)
        entry.insert(0, str(self.default_params['brake_chute_area']))
        entry.grid(row=chute_row, column=1, padx=5, pady=2)
        self.entries['brake_chute_area'] = entry
        chute_row += 1
        
        # Коэффициент C тормозного парашюта
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['coeff_c'])
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['coeff_c'] = label
        
        entry = ttk.Entry(chute_frame, width=15)
        entry.insert(0, str(self.default_params['brake_chute_coeff']))
        entry.grid(row=chute_row, column=1, padx=5, pady=2)
        self.entries['brake_chute_coeff'] = entry
        chute_row += 1
        
        # Скорость открытия тормозного парашюта
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['deploy_vel'])
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['deploy_vel'] = label
        
        entry = ttk.Entry(chute_frame, width=15)
        entry.insert(0, str(self.default_params['brake_chute_deploy_velocity']))
        entry.grid(row=chute_row, column=1, padx=5, pady=2)
        self.entries['brake_chute_deploy_velocity'] = entry
        chute_row += 1
        
        # Скорость отстрела тормозного парашюта
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['jettison_vel'])
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=2)
        self.labels['jettison_vel'] = label
        
        entry = ttk.Entry(chute_frame, width=15)
        entry.insert(0, str(self.default_params['brake_chute_jettison_velocity']))
        entry.grid(row=chute_row, column=1, padx=5, pady=2)
        self.entries['brake_chute_jettison_velocity'] = entry
        chute_row += 1

        # Основной парашют
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['main_parachute'], font=('TkDefaultFont', 9, 'bold'))
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=5)
        self.labels['main_parachute'] = label
        chute_row += 1
        
        # Площадь основного парашюта
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['area'])
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=2)
        
        entry = ttk.Entry(chute_frame, width=15)
        entry.insert(0, str(self.default_params['main_chute_area']))
        entry.grid(row=chute_row, column=1, padx=5, pady=2)
        self.entries['main_chute_area'] = entry
        chute_row += 1
        
        # Коэффициент C основного парашюта
        label = ttk.Label(chute_frame, text=self.languages[self.current_lang]['coeff_c'])
        label.grid(row=chute_row, column=0, sticky="w", padx=5, pady=2)
        
        entry = ttk.Entry(chute_frame, width=15)
        entry.insert(0, str(self.default_params['main_chute_coeff']))
        entry.grid(row=chute_row, column=1, padx=5, pady=2)
        self.entries['main_chute_coeff'] = entry
        chute_row += 1
        
        row += 1

        # Параметры моделирования
        params_labels = [
            ('C', self.languages[self.current_lang]['drag_coeff']),
            ('A', self.languages[self.current_lang]['cross_section']),
            ('t_end', self.languages[self.current_lang]['sim_time']),
            ('A_heat_shield', self.languages[self.current_lang]['heat_shield_area']),
            ('c_solid', self.languages[self.current_lang]['specific_heat']),
            ('L', self.languages[self.current_lang]['latent_heat']),
            ('T_melt', self.languages[self.current_lang]['melt_temp']),
            ('T_max', self.languages[self.current_lang]['max_temp']),
            ('T_initial', self.languages[self.current_lang]['init_temp']),
            ('heat_shield_density', self.languages[self.current_lang]['heat_shield_density']),
            ('heat_shield_thickness', self.languages[self.current_lang]['heat_shield_thickness'])
        ]
        
        for key, label_text in params_labels:
            label = ttk.Label(input_frame, text=label_text)
            label.grid(row=row, column=0, sticky="w", pady=3)
            self.labels[key] = label
            
            entry = ttk.Entry(input_frame, width=15)
            entry.insert(0, str(self.default_params[key]))
            entry.grid(row=row, column=1, padx=5, pady=3)
            self.entries[key] = entry
            row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Прогресс бар и статус
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        self.status_label = ttk.Label(self.root, text=self.languages[self.current_lang]['ready'])
        self.status_label.pack()

        # Кнопки
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.run_sim_btn = ttk.Button(button_frame, text=self.languages[self.current_lang]['run_sim'], 
                  command=self.start_simulation)
        self.run_sim_btn.pack(side=tk.LEFT, padx=5)
        self.labels['run_sim'] = self.run_sim_btn
        
        self.default_btn = ttk.Button(button_frame, text=self.languages[self.current_lang]['default_params'], 
                  command=self.set_default_params)
        self.default_btn.pack(side=tk.LEFT, padx=5)
        self.labels['default_params'] = self.default_btn
        
        self.density_btn = ttk.Button(button_frame, text=self.languages[self.current_lang]['show_density'], 
                  command=self.show_density_plot)
        self.density_btn.pack(side=tk.LEFT, padx=5)
        self.labels['show_density'] = self.density_btn
        
        # Кнопка смены языка
        self.lang_btn = ttk.Button(button_frame, text=self.languages[self.current_lang]['change_lang'],
                                 command=self.toggle_language)
        self.lang_btn.pack(side=tk.LEFT, padx=5)
        self.labels['change_lang'] = self.lang_btn

        self.calculate_velocity_components()
        self.toggle_mass_fields()
        self.toggle_parachute_fields()
    
    def toggle_language(self):
        """Переключение языка интерфейса"""
        self.current_lang = 'en' if self.current_lang == 'ru' else 'ru'
        self.update_language()
    
    def update_language(self):
        """Обновление всех текстовых элементов интерфейса"""
        lang = self.languages[self.current_lang]
        
        self.root.title(lang['title'])
        
        # Обновление всех меток
        for key, widget in self.labels.items():
            if isinstance(widget, ttk.Label):
                widget.config(text=lang.get(key, widget.cget('text')))
            elif isinstance(widget, ttk.Button):
                widget.config(text=lang.get(key, widget.cget('text')))
            elif isinstance(widget, ttk.Radiobutton):
                widget.config(text=lang.get(key, widget.cget('text')))
            elif isinstance(widget, ttk.Checkbutton):
                widget.config(text=lang.get(key, widget.cget('text')))
        
        # Обновление заголовков фреймов
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Canvas):
                        for canvas_child in subchild.winfo_children():
                            if isinstance(canvas_child, ttk.Frame):
                                for frame_child in canvas_child.winfo_children():
                                    if isinstance(frame_child, ttk.LabelFrame):
                                        title_key = None
                                        if frame_child.cget('text') == self.languages['ru']['sim_params']:
                                            title_key = 'sim_params'
                                        elif frame_child.cget('text') == self.languages['ru']['init_conditions']:
                                            title_key = 'init_conditions'
                                        elif frame_child.cget('text') == self.languages['ru']['mass_calc_mode']:
                                            title_key = 'mass_calc_mode'
                                        elif frame_child.cget('text') == self.languages['ru']['parachute_system']:
                                            title_key = 'parachute_system'
                                        
                                        if title_key:
                                            frame_child.config(text=lang[title_key])
        
        # Обновление статуса
        self.status_label.config(text=lang['ready'])
    
    def toggle_mass_fields(self):
        mode = self.mass_mode_var.get()
        
        if mode == 'specified':
            self.entries['m'].config(state='normal')
            self.entries['envelope_density'].config(state='disabled')
            self.entries['payload_mass'].config(state='disabled')
            self.entries['gas_lift_per_m3'].config(state='disabled')
        else: 
            self.entries['m'].config(state='disabled')
            self.entries['envelope_density'].config(state='normal')
            self.entries['payload_mass'].config(state='normal')
            self.entries['gas_lift_per_m3'].config(state='normal')
    
    def toggle_parachute_fields(self):
        state = 'normal' if self.use_parachute_var.get() else 'disabled'
        
        parachute_params = ['brake_chute_area', 'brake_chute_coeff', 'brake_chute_deploy_velocity',
                           'brake_chute_jettison_velocity', 'main_chute_area', 'main_chute_coeff']
        
        for param in parachute_params:
            if param in self.entries:
                self.entries[param].config(state=state)
    
    def calculate_velocity_components(self):
        try:
            import math
            
            entry_angle = float(self.entries['entry_angle'].get())
            entry_speed = float(self.entries['v0'].get())
            h0 = float(self.entries['h0'].get())
            
            if not (0 <= entry_angle <= 90):
                if self.current_lang == 'ru':
                    messagebox.showwarning("Предупреждение", "Угол входа должен быть от 0 до 90 градусов")
                else:
                    messagebox.showwarning("Warning", "Entry angle must be between 0 and 90 degrees")
                return
           
            angle_rad = math.radians(entry_angle)
            
            vx = entry_speed * math.cos(angle_rad)  
            vy = -entry_speed * math.sin(angle_rad)  
      
            self.vx_display.config(state='normal')
            self.vx_display.delete(0, tk.END)
            self.vx_display.insert(0, f"{vx:.2f}")
            self.vx_display.config(state='readonly')
            
            self.vy_display.config(state='normal')
            self.vy_display.delete(0, tk.END)
            self.vy_display.insert(0, f"{vy:.2f}")
            self.vy_display.config(state='readonly')
            
            if self.current_lang == 'ru':
                self.status_label.config(text=f"Рассчитано: vx={vx:.0f} м/с, vy={vy:.0f} м/с, h={h0/1000:.0f} км")
            else:
                self.status_label.config(text=f"Calculated: vx={vx:.0f} m/s, vy={vy:.0f} m/s, h={h0/1000:.0f} km")
            
        except ValueError as e:
            if self.current_lang == 'ru':
                messagebox.showerror("Ошибка", f"Введите корректные числовые значения: {str(e)}")
            else:
                messagebox.showerror("Error", f"Enter valid numeric values: {str(e)}")
    
    def show_density_plot(self):
        from materials import plot_density_profile
        import matplotlib.pyplot as plt
        
        try:
            fig = plot_density_profile()
            plt.show()
        except Exception as e:
            if self.current_lang == 'ru':
                messagebox.showerror("Ошибка", f"Не удалось построить график плотности:\n{str(e)}")
            else:
                messagebox.showerror("Error", f"Failed to plot density profile:\n{str(e)}")
    
    def get_params(self):
        params = []
        param_keys = ['C', 'A', 'm', 'h0', 'v0', 'entry_angle', 't_end', 'A_heat_shield',
                     'c_solid', 'L', 'T_melt', 'T_max', 'T_initial', 'heat_shield_density', 
                     'heat_shield_thickness']
        
        for key in param_keys:
            try:
                value = float(self.entries[key].get())
                params.append(value)
            except ValueError:
                params.append(self.default_params[key])
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, str(self.default_params[key]))
                if self.current_lang == 'ru':
                    messagebox.showwarning("Предупреждение", 
                                         f"Некорректное значение для '{key}'. Использовано значение по умолчанию: {self.default_params[key]}")
                else:
                    messagebox.showwarning("Warning", 
                                         f"Invalid value for '{key}'. Using default: {self.default_params[key]}")

        envelope_density = float(self.entries['envelope_density'].get())
        payload_mass = float(self.entries['payload_mass'].get())
        gas_lift_per_m3 = float(self.entries['gas_lift_per_m3'].get())
        
        params.append(envelope_density)
        params.append(payload_mass)
        params.append(gas_lift_per_m3)

        mass_mode = self.mass_mode_var.get()
        params.append(1 if mass_mode == 'airship' else 0)

        use_parachute = self.use_parachute_var.get()
        params.append(int(use_parachute)) 

        parachute_keys = ['brake_chute_area', 'brake_chute_coeff', 
                         'brake_chute_deploy_velocity', 'main_chute_area',
                         'main_chute_coeff', 'brake_chute_jettison_velocity']
        
        for key in parachute_keys:
            try:
                if use_parachute:
                    value = float(self.entries[key].get())
                else:
                    value = self.default_params[key]
                params.append(value)
            except ValueError:
                params.append(self.default_params[key])
                if use_parachute:
                    self.entries[key].delete(0, tk.END)
                    self.entries[key].insert(0, str(self.default_params[key]))
                    if self.current_lang == 'ru':
                        messagebox.showwarning("Предупреждение", 
                                             f"Некорректное значение для '{key}'. Использовано значение по умолчанию: {self.default_params[key]}")
                    else:
                        messagebox.showwarning("Warning", 
                                             f"Invalid value for '{key}'. Using default: {self.default_params[key]}")
        return params
    
    def set_default_params(self):
        for key, value in self.default_params.items():
            if key in self.entries:
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, str(value))
        
        self.use_parachute_var.set(self.default_params['use_parachute'])
        self.mass_mode_var.set(self.default_params['mass_calculation_mode'])
        
        self.toggle_mass_fields()
        self.toggle_parachute_fields()

        self.calculate_velocity_components()
    
    def update_progress(self, value, message):
        self.progress['value'] = value
        self.status_label['text'] = message
        self.root.update()
    
    def start_simulation(self):
        self.disable_buttons()
        
        self.calculate_velocity_components()
       
        self.progress['value'] = 0
        if self.current_lang == 'ru':
            self.status_label['text'] = "Начало расчета..."
        else:
            self.status_label['text'] = "Starting calculation..."
        
        thread = threading.Thread(target=self.run_simulation_thread)
        thread.start()
    
    def disable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        child.config(state='disabled')
    
    def run_simulation_thread(self):
        try:
            params = self.get_params()
            
            print(f"Получено параметров: {len(params)}")
            
            if len(params) != 26:
                if self.current_lang == 'ru':
                    error_msg = f"Неправильное количество параметров: {len(params)} вместо 26"
                else:
                    error_msg = f"Wrong number of parameters: {len(params)} instead of 26"
                self.root.after(0, self.show_error, error_msg)
                return
            
            h0 = params[3] 
            if h0 <= 0:
                if self.current_lang == 'ru':
                    error_msg = "Высота входа должна быть больше 0"
                else:
                    error_msg = "Entry height must be greater than 0"
                self.root.after(0, self.show_error, error_msg)
                return
            
            v0 = params[4]
            if v0 <= 0:
                if self.current_lang == 'ru':
                    error_msg = "Скорость входа должна быть больше 0"
                else:
                    error_msg = "Entry speed must be greater than 0"
                self.root.after(0, self.show_error, error_msg)
                return
            
            entry_angle = params[5] 
            if not (0 <= entry_angle <= 90):
                if self.current_lang == 'ru':
                    error_msg = "Угол входа должен быть от 0 до 90 градусов"
                else:
                    error_msg = "Entry angle must be between 0 and 90 degrees"
                self.root.after(0, self.show_error, error_msg)
                return
            
            use_parachute = bool(params[19])  
            if use_parachute:
                brake_chute_deploy_velocity = params[22] 
                brake_chute_jettison_velocity = params[25]
                
                if not (brake_chute_jettison_velocity < brake_chute_deploy_velocity):
                    if self.current_lang == 'ru':
                        error_msg = ("Скорости парашютов должны удовлетворять:\n"
                                  "Скорость отстрела < Скорость открытия тормозного\n\n"
                                  f"Текущие значения:\n"
                                  f"Отстрел: {brake_chute_jettison_velocity} м/с\n"
                                  f"Открытие тормозного: {brake_chute_deploy_velocity} м/с")
                    else:
                        error_msg = ("Parachute velocities must satisfy:\n"
                                  "Jettison velocity < Brake parachute deployment velocity\n\n"
                                  f"Current values:\n"
                                  f"Jettison: {brake_chute_jettison_velocity} m/s\n"
                                  f"Brake deployment: {brake_chute_deploy_velocity} m/s")
                    self.root.after(0, self.show_error, error_msg)
                    return
            else:
                print("Парашюты не используются")
            
            results = run_simulation(params, self.update_progress)
            self.root.after(0, self.show_results, results, params)
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Ошибка в потоке: {str(e)}\n{error_details}")
            self.root.after(0, self.show_error, f"{str(e)}\n\n{error_details}")
        finally:
            self.root.after(0, self.enable_buttons)
    
    def show_results(self, results, params):
        if self.results_window:
            try:
                self.results_window.window.destroy()
            except:
                pass
        
        results['current_lang'] = self.current_lang
        self.results_window = ResultsWindow(self.root, results, params, self.current_lang)
        
        self.progress['value'] = 0
        if self.current_lang == 'ru':
            self.status_label['text'] = "Расчет завершен"
        else:
            self.status_label['text'] = "Calculation completed"
    
    def show_error(self, error_msg):
        if self.current_lang == 'ru':
            title = "Ошибка моделирования"
        else:
            title = "Simulation Error"
        messagebox.showerror(title, f"{error_msg}")
        self.progress['value'] = 0
        if self.current_lang == 'ru':
            self.status_label['text'] = "Ошибка"
        else:
            self.status_label['text'] = "Error"
    
    def enable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        child.config(state='normal')