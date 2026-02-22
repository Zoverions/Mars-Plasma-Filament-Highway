import numpy as np
import matplotlib.pyplot as plt
import os

class VacuumTNT:
    def __init__(self, tube_pressure_pa=100, capsule_mass_kg=1000, cross_section_area=2.0):
        self.pressure = tube_pressure_pa
        self.mass = capsule_mass_kg
        self.area = cross_section_area
        self.cd = 0.2  # Drag coefficient
        self.rho_air_sl = 1.225 # kg/m^3 at sea level

    def air_density(self):
        # Approximate density at given pressure (assuming ideal gas at constant temp)
        # P = rho * R * T
        # rho = P / (R * T)
        # Ratio rho / rho0 = P / P0
        p0 = 101325 # Pa
        return self.rho_air_sl * (self.pressure / p0)

    def power_consumption(self, velocity):
        # Aerodynamic drag: F_d = 0.5 * rho * v^2 * Cd * A
        rho = self.air_density()
        f_drag = 0.5 * rho * velocity**2 * self.cd * self.area

        # Magnetic drag (induced): F_mag ~ 1/v at high speed, but let's approximate as constant or small for now
        # Or proportional to lift? F_mag = (L/D)_mag * W
        # Let's assume a highly efficient maglev with L/D of 100
        f_mag = (self.mass * 9.81) / 100

        # Total force
        f_total = f_drag + f_mag

        # Power = Force * Velocity
        power = f_total * velocity
        return power

def main():
    # Simulation parameters
    velocities = np.linspace(10, 1000, 100) # m/s (up to ~Mach 3)

    # Compare different pressures
    pressures = [0.1, 10, 100, 1000] # Pa (100 Pa ~ 1 mbar, 0.1 Pa ~ high vacuum)

    plt.figure(figsize=(10, 6))

    for p in pressures:
        tnt = VacuumTNT(tube_pressure_pa=p)
        power = tnt.power_consumption(velocities)
        plt.plot(velocities, power / 1000, label=f'Pressure = {p} Pa')

    plt.title('Vacuum TNT Power Consumption vs Speed')
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Power (kW)')
    plt.yscale('log')
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.legend()

    # Save plot
    output_dir = '../docs/images'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'vacuum_scaling.png')
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    main()
