import numpy as np

def calculate_airship_mass(envelope_density, payload_mass, gas_lift_per_m3, 
                          heat_shield_thickness, heat_shield_density, heat_shield_area):
    heat_shield_mass = heat_shield_area * heat_shield_thickness * heat_shield_density
    
    if gas_lift_per_m3 <= 0:
        R = 5.0 
    else:
        total_mass_for_lift = payload_mass
        R = (total_mass_for_lift / (gas_lift_per_m3 * (4.0/3.0) * np.pi))**(1.0/3.0)
        for _ in range(5):
            surface_area = 4.0 * np.pi * R**2
            envelope_mass = envelope_density * surface_area
            total_mass_for_lift = envelope_mass + payload_mass
            R_new = (total_mass_for_lift / (gas_lift_per_m3 * (4.0/3.0) * np.pi))**(1.0/3.0)
            if abs(R_new - R) < 0.01:
                break
            R = R_new
    
    R = max(R, 0.5)
    volume = (4.0/3.0) * np.pi * R**3
    surface_area = 4.0 * np.pi * R**2
    
    envelope_mass = envelope_density * surface_area
    
    total_mass_for_lift = envelope_mass + payload_mass
    
    lift_force = gas_lift_per_m3 * volume * 9.81
    weight_force = total_mass_for_lift * 9.81
    
    total_mass = total_mass_for_lift + heat_shield_mass
    
    return {
        'total_mass': total_mass,
        'volume': volume,
        'radius': R,
        'envelope_mass': envelope_mass,
        'heat_shield_mass': heat_shield_mass,
        'surface_area': surface_area,
        'lift_force': lift_force,
        'weight_force': weight_force,
        'payload_mass': payload_mass,
        'total_mass_for_lift': total_mass_for_lift
    }