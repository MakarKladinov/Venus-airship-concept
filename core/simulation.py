import numpy as np
from typing import Dict, Tuple, List, Optional, Callable, Any
from dataclasses import dataclass
import logging

# Исправленный импорт - используем относительный импорт
from .materials import VenusAtmosphere, DragExponentModel
from .physics import PhysicsEngine, VehicleParameters, InitialConditions
from .thermal import ThermalCalculator, ThermalProperties, ThermalLoad
from .structure import calculate_airship_mass, calculate_nose_radius_from_area
from .orbital import calculate_orbital_trajectory

logger = logging.getLogger(__name__)

@dataclass
class ParachuteSystem:
    use_parachutes: bool = False
    brake_chute_area: float = 4.0
    main_chute_area: float = 40.0
    brake_chute_coeff: float = 0.8
    main_chute_coeff: float = 1.2
    brake_deploy_velocity: float = 400.0
    brake_jettison_velocity: float = 50.0
    main_deploy_velocity: float = 50.0

@dataclass
class SimulationInput:
    drag_coefficient: float = 0.3
    cross_section_area: float = 1.5
    mass_specified: float = 750.0
    entry_height: float = 250000.0
    entry_speed: float = 7500.0
    entry_angle: float = 12.0
    simulation_time: float = 400.0
    heat_shield_area: float = 1.5
    thermal_properties: ThermalProperties = ThermalProperties()
    mass_calculation_mode: str = 'airship'
    envelope_density: float = 0.8
    payload_mass: float = 150.0
    gas_lift: float = 1.0
    parachute_system: ParachuteSystem = ParachuteSystem()
    integration_step: float = 0.001

@dataclass
class SimulationOutput:
    time: np.ndarray
    velocity_x: np.ndarray
    velocity_y: np.ndarray
    velocity_total: np.ndarray
    height: np.ndarray
    heat_flux: np.ndarray
    n_exponent: np.ndarray
    theta: np.ndarray
    radius: np.ndarray
    velocity_theta: np.ndarray
    velocity_radial: np.ndarray
    latitude: np.ndarray
    longitude: np.ndarray
    flight_distance: float
    flight_time: float
    final_velocity: float
    final_height: float
    thermal_load: ThermalLoad
    parachute_events: Dict[str, Any]
    parachute_states: List[str]
    airship_results: Optional[Dict] = None
    vehicle_mass: float = 0.0
    max_heat_flux: float = 0.0
    angular_displacement: float = 0.0
    arc_distance: float = 0.0

class SimulationEngine:
    
    def __init__(self):
        self.atmosphere = VenusAtmosphere()
        self.drag_model = DragExponentModel()
        self.physics = PhysicsEngine(self.atmosphere, self.drag_model)
        self.thermal = ThermalCalculator()
        self.integration_step = 0.001
    
    def run(self, input_data: SimulationInput, progress_callback: Optional[Callable] = None) -> SimulationOutput:
        logger.info("Starting simulation...")
        
        if progress_callback:
            progress_callback(0, "Initializing simulation...")
        
        vehicle_mass, airship_results = self._calculate_vehicle_mass(input_data)
        
        if progress_callback:
            progress_callback(10, f"Vehicle mass: {vehicle_mass:.1f} kg")
        
        init_conditions = InitialConditions(
            entry_height=input_data.entry_height,
            entry_velocity=input_data.entry_speed,
            entry_angle=input_data.entry_angle
        )
        
        nose_radius = calculate_nose_radius_from_area(input_data.cross_section_area)
        vehicle = VehicleParameters(
            mass=vehicle_mass,
            drag_coefficient=input_data.drag_coefficient,
            cross_section_area=input_data.cross_section_area,
            nose_radius=nose_radius
        )
        
        if progress_callback:
            progress_callback(15, "Integrating trajectory...")
        
        trajectory_results = self._integrate_trajectory(
            init_conditions, vehicle, input_data, progress_callback
        )
        
        if progress_callback:
            progress_callback(85, "Calculating thermal loads...")
        
        thermal_load = self._calculate_thermal_loads(
            trajectory_results, input_data
        )
        
        if progress_callback:
            progress_callback(90, "Calculating orbital parameters...")
        
        orbital_results = calculate_orbital_trajectory(
            trajectory_results['time'],
            trajectory_results['vx'],
            trajectory_results['vy'],
            trajectory_results['height']
        )
        
        if progress_callback:
            progress_callback(95, "Compiling results...")
        
        output = self._compile_output(
            trajectory_results,
            thermal_load,
            orbital_results,
            input_data,
            vehicle_mass,
            airship_results,
            init_conditions
        )
        
        if progress_callback:
            progress_callback(100, "Simulation completed")
        
        logger.info("Simulation completed successfully")
        return output
    
    def _calculate_vehicle_mass(self, input_data: SimulationInput) -> Tuple[float, Optional[Dict]]:
        if input_data.mass_calculation_mode == 'airship':
            results = calculate_airship_mass(
                envelope_density=input_data.envelope_density,
                payload_mass=input_data.payload_mass,
                gas_lift=input_data.gas_lift,
                heat_shield_thickness=input_data.thermal_properties.thickness,
                heat_shield_density=input_data.thermal_properties.density,
                heat_shield_area=input_data.heat_shield_area
            )
            return results['total_mass'], results
        else:
            return input_data.mass_specified, None
    
    def _integrate_trajectory(self, init_conditions, vehicle, input_data, progress_callback):
        n_steps = int(input_data.simulation_time / self.integration_step) + 1
        
        time = np.zeros(n_steps)
        vx = np.zeros(n_steps)
        vy = np.zeros(n_steps)
        height = np.zeros(n_steps)
        n_exp = np.zeros(n_steps)
        parachute_states = ['none'] * n_steps
        
        time[0] = 0.0
        vx[0] = init_conditions.vx0
        vy[0] = init_conditions.vy0
        height[0] = init_conditions.entry_height
        
        parachute_params = {
            'brake_area': input_data.parachute_system.brake_chute_area,
            'brake_coeff': input_data.parachute_system.brake_chute_coeff,
            'main_area': input_data.parachute_system.main_chute_area,
            'main_coeff': input_data.parachute_system.main_chute_coeff
        }
        
        brake_deployed = False
        main_deployed = False
        brake_jettisoned = False
        parachute_events = {}
        
        for i in range(n_steps - 1):
            current_time = time[i]
            current_vx = vx[i]
            current_vy = vy[i]
            current_height = height[i]
            current_v_total = np.sqrt(current_vx**2 + current_vy**2)
            
            parachute_state = self._determine_parachute_state(
                current_v_total,
                input_data.parachute_system,
                brake_deployed,
                main_deployed,
                brake_jettisoned,
                parachute_events,
                current_time,
                current_height
            )
            
            if parachute_state == 'brake' and not brake_deployed:
                brake_deployed = True
            elif parachute_state == 'main' and not main_deployed:
                main_deployed = True
            elif 'brake_jettison' in parachute_events and not brake_jettisoned:
                brake_jettisoned = True
            
            parachute_states[i] = parachute_state
            
            if input_data.parachute_system.use_parachutes and parachute_state != 'none':
                ax, ay, v_total = self.physics.calculate_acceleration_with_parachutes(
                    current_vx, current_vy, current_height,
                    vehicle, parachute_state, parachute_params
                )
            else:
                ax, ay, v_total = self.physics.calculate_acceleration(
                    current_vx, current_vy, current_height, vehicle
                )
            
            n_exp[i] = self.drag_model.n_value(v_total)
            
            vx[i+1] = current_vx + ax * self.integration_step
            vy[i+1] = current_vy + ay * self.integration_step
            height[i+1] = current_height + current_vy * self.integration_step
            time[i+1] = current_time + self.integration_step
            
            if height[i+1] <= 0:
                height[i+1] = 0
                vx[i+1] = 0
                vy[i+1] = 0
                n_steps = i + 2
                break
            
            if v_total < 1.0 and current_height < 1000:
                n_steps = i + 1
                break
            
            if progress_callback and i % 1000 == 0:
                progress = min(80, 15 + 65 * i / n_steps)
                progress_callback(progress, f"Step {i}/{n_steps}")
        
        time = time[:n_steps]
        vx = vx[:n_steps]
        vy = vy[:n_steps]
        height = height[:n_steps]
        n_exp = n_exp[:n_steps]
        parachute_states = parachute_states[:n_steps]
        
        v_total = np.sqrt(vx**2 + vy**2)
        
        return {
            'time': time,
            'vx': vx,
            'vy': vy,
            'height': height,
            'n_exp': n_exp,
            'v_total': v_total,
            'parachute_states': parachute_states,
            'parachute_events': parachute_events
        }
    
    def _determine_parachute_state(self, velocity, parachute_system, brake_deployed, main_deployed, brake_jettisoned, events, time, height):
        if not parachute_system.use_parachutes:
            return 'none'
        
        if not brake_deployed and velocity <= parachute_system.brake_deploy_velocity:
            events['brake_deploy_time'] = time
            events['brake_deploy_velocity'] = velocity
            events['brake_deploy_height'] = height
            return 'brake'
        
        if brake_deployed and not main_deployed and velocity <= parachute_system.main_deploy_velocity:
            events['main_deploy_time'] = time
            events['main_deploy_velocity'] = velocity
            events['main_deploy_height'] = height
            return 'both'
        
        if brake_deployed and not brake_jettisoned and velocity <= parachute_system.brake_jettison_velocity:
            events['brake_jettison_time'] = time
            events['brake_jettison_velocity'] = velocity
            events['brake_jettison_height'] = height
            return 'main'
        
        if brake_deployed:
            if not brake_jettisoned:
                if main_deployed:
                    return 'both'
                else:
                    return 'brake'
            else:
                if main_deployed:
                    return 'main'
        
        return 'none'
    
    def _calculate_thermal_loads(self, trajectory_results, input_data):
        time = trajectory_results['time']
        v_total = trajectory_results['v_total']
        height = trajectory_results['height']
        
        densities = np.array([self.atmosphere.density(h) for h in height])
        heat_flux = np.array([
            self.thermal.calculate_heat_flux(v, rho, input_data.drag_coefficient)
            for v, rho in zip(v_total, densities)
        ])
        
        thermal_load = self.thermal.calculate_ablation(
            time, heat_flux, input_data.thermal_properties
        )
        
        return thermal_load
    
    def _compile_output(self, trajectory_results, thermal_load, orbital_results, input_data, vehicle_mass, airship_results, init_conditions):
        time = trajectory_results['time']
        vx = trajectory_results['vx']
        vy = trajectory_results['vy']
        height = trajectory_results['height']
        v_total = trajectory_results['v_total']
        n_exp = trajectory_results['n_exp']
        
        densities = np.array([self.atmosphere.density(h) for h in height])
        heat_flux = np.array([
            self.thermal.calculate_heat_flux(v, rho, input_data.drag_coefficient)
            for v, rho in zip(v_total, densities)
        ])
        
        flight_time = time[-1] if len(time) > 0 else 0
        final_velocity = v_total[-1] if len(v_total) > 0 else 0
        final_height = height[-1] if len(height) > 0 else 0
        
        flight_distance = 0.0
        if len(time) > 1:
            for i in range(len(time) - 1):
                dt = time[i+1] - time[i]
                vx_avg = (vx[i] + vx[i+1]) / 2.0
                flight_distance += vx_avg * dt
        
        theta, radius, v_theta, v_r, latitude, longitude = orbital_results
        
        angular_displacement = 0.0
        if len(theta) > 0:
            angular_displacement = theta[-1] - theta[0]
        
        arc_distance = angular_displacement * radius[-1] if len(radius) > 0 else 0
        
        return SimulationOutput(
            time=time,
            velocity_x=vx,
            velocity_y=vy,
            velocity_total=v_total,
            height=height,
            heat_flux=heat_flux,
            n_exponent=n_exp,
            theta=theta,
            radius=radius,
            velocity_theta=v_theta,
            velocity_radial=v_r,
            latitude=latitude,
            longitude=longitude,
            flight_distance=flight_distance,
            flight_time=flight_time,
            final_velocity=final_velocity,
            final_height=final_height,
            thermal_load=thermal_load,
            parachute_events=trajectory_results.get('parachute_events', {}),
            parachute_states=trajectory_results.get('parachute_states', []),
            airship_results=airship_results,
            vehicle_mass=vehicle_mass,
            max_heat_flux=np.max(heat_flux) if len(heat_flux) > 0 else 0.0,
            angular_displacement=angular_displacement,
            arc_distance=arc_distance
        )