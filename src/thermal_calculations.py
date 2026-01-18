import numpy as np

def calculate_heat_flux(v_total, rho, C):
    K = 10e-4
    v_abs = abs(v_total)
    q = K * rho * (v_abs ** 3)
    return q

def calculate_total_heat(t, q, A_heat_shield):
    Q_total = 0.0
    Q_per_area = 0.0
    
    if len(t) > 1 and len(q) > 1:
        for i in range(len(t) - 1):
            dt = t[i+1] - t[i]
            q_avg = (q[i] + q[i+1]) / 2.0
            Q_per_area += q_avg * dt
        
        Q_total = Q_per_area * A_heat_shield
    
    return Q_total, Q_per_area

def calculate_temperature(Q_per_area, m_per_area, c, T_initial):
    if m_per_area > 0 and c > 0:
        delta_T = Q_per_area / (m_per_area * c)
        T_final = T_initial + delta_T
        return T_final, delta_T
    return T_initial, 0

def calculate_melting(Q_per_area, m_per_area, c_solid, L, T_melt, T_initial):
    if m_per_area <= 0 or c_solid <= 0:
        return T_initial, 0.0, 0.0
    
    energy_to_melt = m_per_area * c_solid * (T_melt - T_initial)
    
    if Q_per_area <= energy_to_melt:
        T_final = T_initial + Q_per_area / (m_per_area * c_solid)
        melted_fraction = 0.0
        melted_mass = 0.0
    else:
        remaining_energy = Q_per_area - energy_to_melt
        T_final = T_melt
        
        energy_for_full_melt = m_per_area * L
        
        if remaining_energy <= energy_for_full_melt:
            melted_mass = remaining_energy / L
            melted_fraction = melted_mass / m_per_area
        else:
            melted_mass = m_per_area
            melted_fraction = 1.0
            T_final = T_melt + (remaining_energy - energy_for_full_melt) / (m_per_area * c_solid * 1.5)
    
    return T_final, melted_fraction, melted_mass