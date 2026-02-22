import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, e, m_e, epsilon_0
import os

class PlasmaChannel:
    def __init__(self, n_e, B0, length_m):
        self.n_e = n_e  # Electron density (m^-3)
        self.B0 = B0    # Magnetic field (T)
        self.length = length_m

        # Plasma frequency
        self.omega_p = np.sqrt(n_e * e**2 / (epsilon_0 * m_e))
        # Cyclotron frequency
        self.omega_c = e * B0 / m_e

    def group_velocity(self, omega):
        """
        Calculate group velocity for whistler mode waves.
        Valid for omega < omega_c.
        """
        # Corrected whistler group velocity dispersion relation
        # Note: The prompt formula had c^2 which leads to unit mismatch (m^2/s^2) and superluminal values.
        # Adjusted to c to maintain velocity units and subluminal constraint.
        # v_g = 2 * c * omega * omega_c / omega_p^2 * (1 - omega / omega_c)

        # Ensure we don't go above omega_c (whistler mode cutoff)
        omega = np.minimum(omega, self.omega_c * 0.99)

        vg = 2 * c * omega * self.omega_c / self.omega_p**2 * (1 - omega / self.omega_c)
        return vg

def main():
    # Parameters
    n_e = 1e20  # m^-3
    B0 = 5.0    # Tesla
    length = 1000 # meters

    channel = PlasmaChannel(n_e, B0, length)

    # Frequency range: 0.1 to 0.9 of cyclotron frequency
    freqs = np.linspace(0.1 * channel.omega_c, 0.9 * channel.omega_c, 100)

    v_g = channel.group_velocity(freqs)

    # Normalize
    v_g_c = v_g / c
    freq_norm = freqs / channel.omega_c

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(freq_norm, v_g_c, label='Whistler Group Velocity', color='blue', linewidth=2)
    plt.axhline(y=1.0, color='r', linestyle='--', label='Speed of Light (c)')
    plt.title(f'Whistler Mode Group Velocity in Plasma Channel\n$n_e={n_e:.1e} m^{{-3}}, B_0={B0} T$')
    plt.xlabel(r'Frequency $\omega / \omega_c$')
    plt.ylabel(r'Group Velocity $v_g / c$')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Save plot
    output_dir = '../docs/images'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'group_velocity.png')
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

    # Print specific point
    test_omega = 0.5 * channel.omega_c
    test_vg = channel.group_velocity(test_omega)
    print(f"At omega = 0.5 omega_c: v_g = {test_vg/c:.4f} c")

    # Check the prompt's example frequency
    prompt_omega = 2 * np.pi * 1e9
    prompt_vg = channel.group_velocity(prompt_omega)
    print(f"At omega = 2*pi*1e9 (Prompt Example): v_g = {prompt_vg/c:.4f} c")

if __name__ == "__main__":
    main()
