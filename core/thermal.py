
import numpy as np
from dataclasses import dataclass

@dataclass
class ThermalProperties:
    specific_heat: float = 900.0
    latent_heat: float = 20e6
    melting_temperature: float = 2100.0
    max_temperature: float = 2300.0
    initial_temperature: float = 20.0
    density: float = 600.0
    thickness: float = 0.1
    area: float = 1.5

@dataclass
class ThermalLoad:
    max_heat_flux: float = 0.0
    total_energy: float = 0.0
    energy_per_area: float = 0.0
    surface_temperature: float = 0.0
    ablated_fraction: float = 0.0
    ablated_mass: float = 0.0
    efficiency: float = 0.0

class ThermalCalculator:
    HEAT_FLUX_COEFFICIENT: float = 10e-4
    
    def calculate_heat_flux(self, velocity, density, drag_coefficient=0.3):
        v_abs = abs(velocity)
        return self.HEAT_FLUX_COEFFICIENT * density * (v_abs ** 3) * drag_coefficient
    
    def calculate_total_energy(self, time, heat_flux, heat_shield_area):
        energy_per_area = 0.0
        
        if len(time) > 1 and len(heat_flux) > 1:
            for i in range(len(time) - 1):
                dt = time[i+1] - time[i]
                q_avg = (heat_flux[i] + heat_flux[i+1]) / 2.0
                energy_per_area += q_avg * dt
        
        total_energy = energy_per_area * heat_shield_area
        return total_energy, energy_per_area
    
    def calculate_ablation(self, time, heat_flux, properties):
        mass_per_area = properties.density * properties.thickness
        
        if len(time) <= 1 or mass_per_area <= 0:
            return ThermalLoad()
        
        ablated_mass = 0.0
        current_temp = properties.initial_temperature
        
        for i in range(len(time) - 1):
            dt = time[i+1] - time[i]
            q_avg = (heat_flux[i] + heat_flux[i+1]) / 2.0
            
            if q_avg <= 0:
                continue
            
            energy_in = q_avg * dt
            
            if current_temp < properties.melting_temperature:
                temp_rise = energy_in / (mass_per_area * properties.specific_heat)
                current_temp += temp_rise
                
                if current_temp > properties.melting_temperature:
                    excess_energy = (current_temp - properties.melting_temperature) * mass_per_area * properties.specific_heat
                    current_temp = properties.melting_temperature
                    
                    if excess_energy > 0:
                        ablation_energy = excess_energy
                    else:
                        ablation_energy = 0
                else:
                    ablation_energy = 0
            else:
                ablation_energy = energy_in
            
            if ablation_energy > 0 and current_temp >= properties.melting_temperature:
                mass_ablated = ablation_energy / properties.latent_heat
                ablated_mass += mass_ablated
                mass_per_area -= mass_ablated
                
                if mass_per_area <= 0:
                    mass_per_area = 0
                    ablated_fraction = 1.0
                    break
        
        if properties.density * properties.thickness > 0:
            ablated_fraction = ablated_mass / (properties.density * properties.thickness)
        else:
            ablated_fraction = 0.0
        
        total_energy, energy_per_area = self.calculate_total_energy(time, heat_flux, properties.area)
        
        return ThermalLoad(
            max_heat_flux=np.max(heat_flux) if len(heat_flux) > 0 else 0.0,
            total_energy=total_energy,
            energy_per_area=energy_per_area,
            surface_temperature=current_temp,
            ablated_fraction=ablated_fraction,
            ablated_mass=ablated_mass * properties.area,
            efficiency=self.calculate_efficiency(total_energy, properties)
        )
    
    def calculate_efficiency(self, total_energy, properties):
        heat_shield_mass = properties.density * properties.thickness * properties.area
        max_energy = heat_shield_mass * properties.specific_heat * (properties.max_temperature - properties.initial_temperature)
        
        if total_energy > 0 and max_energy > 0:
            efficiency = min(max_energy, total_energy) / max_energy * 100
        else:
            efficiency = 100.0
        
        return efficiency