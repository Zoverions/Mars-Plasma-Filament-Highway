import numpy as np
import matplotlib.pyplot as plt
import os

class MarsTrajectory:
    def __init__(self, acceleration=0.01):
        self.a = acceleration  # m/s^2
        self.AU = 1.496e11     # meters
        self.d = 2.25 * self.AU # Distance to Mars (approximate average for this trajectory)

    def calculate_transit_time(self):
        # Time to accelerate halfway
        t_half = np.sqrt(self.d / self.a)
        t_total = 2 * t_half
        return t_total

    def plot_trajectory(self):
        t_total = self.calculate_transit_time()
        t_half = t_total / 2

        # Time points
        t = np.linspace(0, t_total, 1000)

        # Velocity and Distance arrays
        v = np.zeros_like(t)
        x = np.zeros_like(t)

        # First half: Acceleration
        mask1 = t <= t_half
        v[mask1] = self.a * t[mask1]
        x[mask1] = 0.5 * self.a * t[mask1]**2

        # Second half: Deceleration
        # v = v_max - a * (t - t_half)
        # x = x_half + v_max * (t - t_half) - 0.5 * a * (t - t_half)^2
        mask2 = t > t_half
        v_max = self.a * t_half
        x_half = 0.5 * self.a * t_half**2

        dt = t[mask2] - t_half
        v[mask2] = v_max - self.a * dt
        x[mask2] = x_half + v_max * dt - 0.5 * self.a * dt**2

        # Plotting
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Time (days)')
        ax1.set_ylabel('Distance (AU)', color=color)
        ax1.plot(t / 86400, x / self.AU, color=color, linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:orange'
        ax2.set_ylabel('Velocity (km/s)', color=color)  # we already handled the x-label with ax1
        ax2.plot(t / 86400, v / 1000, color=color, linewidth=2, linestyle='--')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title(f'Mars Transit Trajectory\nConstant Acceleration a = {self.a} m/s²')
        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        # Save plot
        output_dir = '../docs/images'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'trajectory_mars.png')
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")

        print(f"Total Transit Time: {t_total/86400:.1f} days")
        print(f"Max Velocity: {v_max/1000:.1f} km/s")

if __name__ == "__main__":
    traj = MarsTrajectory()
    traj.plot_trajectory()
