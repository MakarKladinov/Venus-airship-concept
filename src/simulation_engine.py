import numpy as np
from materials import gravity_at_height, density_at_height, temperature_at_height, n_v
from thermal_calculations import calculate_heat_flux, calculate_total_heat, calculate_temperature, calculate_melting
from structure_calculations import calculate_airship_mass

def calculate_radius_from_area(A):
    if A > 0:
        R = np.sqrt(A / np.pi)
    else:
        R = 0.5
    return R

def calculate_acceleration_with_parachutes(vx, vy, h, m, C, A, 
                                         parachute_state, 
                                         brake_chute_area, brake_chute_coeff,
                                         main_chute_area, main_chute_coeff):
    v_total = np.sqrt(vx**2 + vy**2)
    
    g = gravity_at_height(h)
    rho = density_at_height(h)
    
    n = n_v(v_total)
    if v_total > 1e-3:
        force_drag_magnitude = 0.5 * rho * C * A * (v_total ** n)
    else:
        force_drag_magnitude = 0.0
    
    if parachute_state == 'brake':
        force_chute = 0.5 * rho * brake_chute_coeff * brake_chute_area * (v_total ** 2)
        force_drag_magnitude += force_chute
    elif parachute_state == 'main':
        force_chute = 0.5 * rho * main_chute_coeff * main_chute_area * (v_total ** 2)
        force_drag_magnitude += force_chute
    elif parachute_state == 'both':
        force_brake = 0.5 * rho * brake_chute_coeff * brake_chute_area * (v_total ** 2)
        force_main = 0.5 * rho * main_chute_coeff * main_chute_area * (v_total ** 2)
        force_drag_magnitude += force_brake + force_main
    
    if v_total > 1e-3:
        force_drag_x = -force_drag_magnitude * (vx / v_total)
        force_drag_y = -force_drag_magnitude * (vy / v_total)
    else:
        force_drag_x = 0
        force_drag_y = 0
    
    dvx = force_drag_x / m
    dvy = force_drag_y / m - g
    
    return dvx, dvy, v_total

def calculate_acceleration(vx, vy, h, m, C, A):
    v_total = np.sqrt(vx**2 + vy**2)
    
    g = gravity_at_height(h)
    rho = density_at_height(h)
    
    n = n_v(v_total)
    if v_total > 1e-3:
        force_drag_magnitude = 0.5 * rho * C * A * (v_total ** n)
    else:
        force_drag_magnitude = 0.0
    
    if v_total > 1e-3:
        force_drag_x = -force_drag_magnitude * (vx / v_total)
        force_drag_y = -force_drag_magnitude * (vy / v_total)
    else:
        force_drag_x = 0
        force_drag_y = 0
    
    dvx = force_drag_x / m
    dvy = force_drag_y / m - g
    
    return dvx, dvy, v_total

def calculate_impact_distance(t, vx):
    distance = 0.0
    
    if len(t) > 1 and len(vx) > 1:
        for i in range(len(t) - 1):
            dt = t[i+1] - t[i]
            vx_avg = (vx[i] + vx[i+1]) / 2.0
            distance += vx_avg * dt
    
    return distance

def calculate_orbital_trajectory(time, vx, vy, height, R_venus=6051800):
    n = len(time)
    if n == 0:
        return [], [], [], [], []
    
    theta = np.zeros(n)
    r = np.zeros(n)
    v_theta = np.zeros(n)
    v_r = np.zeros(n)
    lat = np.zeros(n)
    lon = np.zeros(n)
    
    r[0] = R_venus + height[0]
    v_r[0] = -vy[0]
    v_theta[0] = vx[0]
    
    for i in range(n):
        r[i] = R_venus + height[i]
        
        if i == 0:
            theta[0] = 0
        else:
            dt = time[i] - time[i-1]
            if r[i-1] > 0:
                angular_velocity = vx[i-1] / r[i-1]
                theta[i] = theta[i-1] + angular_velocity * dt
            else:
                theta[i] = theta[i-1]
        
        v_r[i] = -vy[i]
        if r[i] > 0:
            v_theta[i] = vx[i]
        
        lat[i] = 0
        lon[i] = np.degrees(theta[i]) % 360
    
    return theta, r, v_theta, v_r, lat, lon

def run_simulation(params, progress_callback=None):
    if progress_callback:
        progress_callback(0, "Начало расчета...")
    
    if len(params) != 26:
        raise ValueError(f"Ожидается 26 параметров, получено {len(params)}")
    
    try:
        (C, A, m_specified, h0, v0_total, entry_angle, t_end, A_heat_shield, 
         c_solid, L, T_melt, T_max, T_initial, heat_shield_density, heat_shield_thickness,
         envelope_density, payload_mass, gas_lift_per_m3,
         mass_calculation_mode_int,
         use_parachute_int,
         brake_chute_area, brake_chute_coeff,
         brake_chute_deploy_velocity, main_chute_area,
         main_chute_coeff, brake_chute_jettison_velocity) = params
    except ValueError as e:
        print(f"Ошибка распаковки параметров: {e}")
        print(f"Параметры: {params}")
        raise
    
    mass_calculation_mode = bool(mass_calculation_mode_int)
    use_parachute = bool(use_parachute_int)
    
    dt_integration = 0.001
    
    R_nose = calculate_radius_from_area(A)
    
    if progress_callback:
        progress_callback(5, f"Расчет радиуса полусферы: R={R_nose:.2f} м")
    
    angle_rad = np.radians(entry_angle)
    vx0 = v0_total * np.cos(angle_rad)
    vy0 = -v0_total * np.sin(angle_rad)
    
    if progress_callback:
        progress_callback(10, f"Скорости: vx={vx0:.0f} м/с, vy={vy0:.0f} м/с, h={h0/1000:.0f} км")
    
    if mass_calculation_mode:
        airship_results = calculate_airship_mass(
            envelope_density, payload_mass, gas_lift_per_m3,
            heat_shield_thickness, heat_shield_density, A_heat_shield
        )
        m_calculated = airship_results['total_mass']
        
        if progress_callback:
            progress_callback(15, f"Расчет массы дирижабля: {m_calculated:.1f} кг")
    else:
        m_calculated = m_specified
        airship_results = {
            'total_mass': m_specified,
            'volume': 0,
            'radius': 0,
            'envelope_mass': 0,
            'heat_shield_mass': heat_shield_density * heat_shield_thickness * A_heat_shield,
            'surface_area': 0,
            'lift_force': 0,
            'weight_force': m_specified * 9.81,
            'payload_mass': payload_mass,
            'total_mass_for_lift': m_specified
        }
        
        if progress_callback:
            progress_callback(15, f"Используется заданная масса: {m_calculated:.1f} кг")
    
    material_properties = {
        'entry_angle': entry_angle,
        'c_solid': c_solid,
        'L': L,
        'T_melt': T_melt,
        'T_max': T_max,
        'T_initial': T_initial,
        'density': heat_shield_density,
        'thickness': heat_shield_thickness,
        'envelope_density': envelope_density,
        'R_nose': R_nose,
        'h0': h0,
        'mass_calculation_mode': 'airship' if mass_calculation_mode else 'specified'
    }
    
    parachute_properties = {
        'use_parachute': use_parachute,
        'brake_chute_area': brake_chute_area,
        'brake_chute_coeff': brake_chute_coeff,
        'brake_chute_deploy_velocity': brake_chute_deploy_velocity,
        'main_chute_area': main_chute_area,
        'main_chute_coeff': main_chute_coeff,
        'main_chute_deploy_velocity': brake_chute_jettison_velocity, 
        'brake_chute_jettison_velocity': brake_chute_jettison_velocity
    }
    
    dt = dt_integration
    n_steps = int(t_end / dt) + 1
    
    time = np.zeros(n_steps)
    vx = np.zeros(n_steps)
    vy = np.zeros(n_steps)
    height = np.zeros(n_steps)
    v_total = np.zeros(n_steps)
    parachute_state_arr = np.zeros(n_steps, dtype='U10')
    
    time[0] = 0.0
    vx[0] = vx0
    vy[0] = vy0
    height[0] = h0
    parachute_state_arr[0] = 'none'
    
    if progress_callback:
        progress_callback(20, f"Начало интегрирования с шагом {dt*1000:.1f} мс...")
    
    progress_update_interval = max(1, n_steps // 100)
    
    brake_chute_deployed = False
    main_chute_deployed = False
    brake_chute_jettisoned = False
    
    parachute_events = {}
    
    for i in range(n_steps - 1):
        t = time[i]
        vx_i = vx[i]
        vy_i = vy[i]
        h_i = height[i]
        v_total_i = np.sqrt(vx_i**2 + vy_i**2)
        
        parachute_state = 'none'
        
        if use_parachute:
            main_chute_deploy_velocity = brake_chute_jettison_velocity
            
            if not brake_chute_deployed and v_total_i <= brake_chute_deploy_velocity:
                brake_chute_deployed = True
                parachute_state = 'brake'
                parachute_events['brake_deploy_time'] = t
                parachute_events['brake_deploy_velocity'] = v_total_i
                parachute_events['brake_deploy_height'] = h_i
                
            
            if not main_chute_deployed and v_total_i <= main_chute_deploy_velocity:
                main_chute_deployed = True
                parachute_events['main_deploy_time'] = t
                parachute_events['main_deploy_velocity'] = v_total_i
                parachute_events['main_deploy_height'] = h_i
                
            
            if not brake_chute_jettisoned and v_total_i <= brake_chute_jettison_velocity:
                brake_chute_jettisoned = True
                parachute_events['brake_jettison_time'] = t
                parachute_events['brake_jettison_velocity'] = v_total_i
                parachute_events['brake_jettison_height'] = h_i
                
            
            if brake_chute_deployed:
                if not brake_chute_jettisoned:
                    if main_chute_deployed:
                        parachute_state = 'both'
                    else:
                        parachute_state = 'brake'
                else:
                    if main_chute_deployed:
                        parachute_state = 'main'
            elif main_chute_deployed:
                parachute_state = 'main'
        
        if use_parachute and parachute_state != 'none':
            dvx, dvy, v_total_calc = calculate_acceleration_with_parachutes(
                vx_i, vy_i, h_i, m_calculated, C, A,
                parachute_state,
                brake_chute_area, brake_chute_coeff,
                main_chute_area, main_chute_coeff
            )
        else:
            dvx, dvy, v_total_calc = calculate_acceleration(vx_i, vy_i, h_i, m_calculated, C, A)
        
        v_total[i] = v_total_calc
        parachute_state_arr[i] = parachute_state
        
        vx[i+1] = vx_i + dvx * dt
        vy[i+1] = vy_i + dvy * dt
        height[i+1] = h_i + vy_i * dt
        time[i+1] = t + dt
        
        if height[i+1] <= 0:
            height[i+1] = 0
            vx[i+1] = 0
            vy[i+1] = 0
            n_steps = i + 2
            time = time[:n_steps]
            vx = vx[:n_steps]
            vy = vy[:n_steps]
            height = height[:n_steps]
            v_total = v_total[:n_steps]
            parachute_state_arr = parachute_state_arr[:n_steps]
            break
            
        if v_total_calc < 1.0 and h_i < 1000:
            n_steps = i + 1
            time = time[:n_steps]
            vx = vx[:n_steps]
            vy = vy[:n_steps]
            height = height[:n_steps]
            v_total = v_total[:n_steps]
            parachute_state_arr = parachute_state_arr[:n_steps]
            break
        
        if progress_callback and i % progress_update_interval == 0:
            progress_percent = 20 + 60 * i / n_steps
            speed_km_s = v_total_calc / 1000
            height_km = h_i / 1000
            
            status_msg = (f"Интегрирование... {i:,}/{n_steps:,} шагов | "
                         f"Скорость: {speed_km_s:.1f} км/с | "
                         f"Высота: {height_km:.0f} км")
            if use_parachute:
                status_msg += f" | Парашют: {parachute_state}"
            progress_callback(progress_percent, status_msg)

    if n_steps > 0:
        if use_parachute and parachute_state_arr[-1] != 'none':
            _, _, v_total_last = calculate_acceleration_with_parachutes(
                vx[-1], vy[-1], height[-1], m_calculated, C, A,
                parachute_state_arr[-1],
                brake_chute_area, brake_chute_coeff,
                main_chute_area, main_chute_coeff
            )
        else:
            _, _, v_total_last = calculate_acceleration(
                vx[-1], vy[-1], height[-1], m_calculated, C, A
            )
        v_total[-1] = v_total_last
    
    if progress_callback:
        progress_callback(85, "Расчет орбитальной траектории...")
    
    theta, r, v_theta, v_r, lat, lon = calculate_orbital_trajectory(time, vx, vy, height)
    
    if progress_callback:
        progress_callback(87, "Расчет тепловых параметров...")
    
    rho_vals = np.array([density_at_height(h) for h in height])
    T_atm_vals = np.array([temperature_at_height(h) for h in height])
    n_vals = np.array([n_v(v) for v in v_total])
    q_vals = np.array([calculate_heat_flux(v, rho, C) 
                      for v, rho in zip(v_total, rho_vals)])
    
    if progress_callback:
        progress_callback(90, "Расчет тепловых параметров...")
    
    Q_total, Q_per_area = calculate_total_heat(time, q_vals, A_heat_shield)
    
    m_per_area = heat_shield_density * heat_shield_thickness
    
    T_simple_final, delta_T = calculate_temperature(
        Q_per_area, m_per_area, c_solid, T_initial
    )
    
    if T_simple_final >= T_melt:
        T_final, melted_fraction, melted_mass = calculate_melting(
            Q_per_area, m_per_area, c_solid, L, T_melt, T_initial
        )
    else:
        T_final = T_simple_final
        melted_fraction = 0.0
        melted_mass = 0.0
    
    m_heat_shield_total = m_per_area * A_heat_shield
    
    distance = calculate_impact_distance(time, vx)
    
    impact_time = time[-1]
    if height[-1] <= 0:
        for i in range(1, len(height)):
            if height[i] <= 0:
                t1, h1 = time[i-1], height[i-1]
                t2, h2 = time[i], height[i]
                impact_time = t1 + (t2 - t1) * (0 - h1) / (h2 - h1)
                break
    
    energy_capacity = m_heat_shield_total * c_solid * (T_max - T_initial)
    heat_shield_efficiency = min(energy_capacity / Q_total, 1.0) * 100 if Q_total > 0 else 0
    
    angular_displacement = theta[-1] if len(theta) > 0 else 0
    arc_distance = angular_displacement * (6051800 + h0)
    
    if not use_parachute:
        parachute_events = {}
    
    if progress_callback:
        progress_callback(95, "Формирование результатов...")
    
    results = {
        'time': time,
        'vx': vx,
        'vy': vy,
        'v_total': v_total,
        'height': height,
        'n_exponent': n_vals,
        'heat_flux': q_vals,
        'total_heat': Q_total,
        'heat_per_area': Q_per_area,
        'heat_shield_mass': m_heat_shield_total,
        'surface_temp_final': T_final,
        'delta_T': delta_T,
        'atm_temp': T_atm_vals,
        'material_props': material_properties,
        'distance': distance,
        'impact_time': impact_time,
        'final_height': height[-1] if len(height) > 0 else 0,
        'final_velocity': v_total[-1] if len(v_total) > 0 else 0,
        'max_heat_flux': np.max(q_vals) if len(q_vals) > 0 else 0,
        'heat_shield_efficiency': heat_shield_efficiency,
        'melted_fraction': melted_fraction * 100,
        'melted_mass': melted_mass * A_heat_shield,
        'm_per_area': m_per_area,
        'energy_capacity': energy_capacity,
        'melting_reached': T_final >= T_melt,
        'max_temp_reached': T_final,
        'airship_results': airship_results,
        'calculated_mass': m_calculated,
        'mass_calculation_mode': mass_calculation_mode,
        'specified_mass': m_specified,
        'theta': theta,
        'r': r,
        'v_theta': v_theta,
        'v_r': v_r,
        'lat': lat,
        'lon': lon,
        'angular_displacement': angular_displacement,
        'arc_distance': arc_distance,
        'R_nose': R_nose,
        'parachute_properties': parachute_properties,
        'parachute_state': parachute_state_arr,
        'parachute_events': parachute_events,
        'brake_chute_deployed': brake_chute_deployed if use_parachute else False,
        'main_chute_deployed': main_chute_deployed if use_parachute else False,
        'brake_chute_jettisoned': brake_chute_jettisoned if use_parachute else False,
        
        'initial_conditions': {
            'entry_angle': entry_angle,
            'v0_total': v0_total,
            'vx0': vx0,
            'vy0': vy0,
            'h0': h0,
            'R_nose': R_nose
        },
        
        'integration_info': {
            'dt_used': dt,
            'n_steps_actual': len(time),
            'simulation_time': time[-1] if len(time) > 0 else 0
        }
    }
    
    if progress_callback:
        progress_callback(100, "Расчет завершен")
    
    return results