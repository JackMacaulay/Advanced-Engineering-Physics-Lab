import matplotlib.pyplot as plt
import numpy as np

# Plot parameters
plt.rcParams['figure.dpi'] = 1000

# Constants
k = 1.38e-23  # Boltzmann's constant in J/K
T = 21+273.15       # Temperature in Kelvin

# Resistance values in Ohms
resistance_values = [50, 0.998e6, 510e3, 250e3, 1.4981e6]

# Function to calculate thermal noise PSD
def thermal_noise_psd(R):
    return np.sqrt(4 * k * T * R)

# Function to format resistance value for label
def format_resistance_label(R):
    if R >= 1e6:  # Mega-Ohms
        return f'{R/1e6} MΩ'
    elif R >= 1e3:  # kilo-Ohms
        return f'{R/1e3} kΩ'
    else:  # Ohms
        return f'{R} Ω'

# Frequency range for plotting (for visual representation only)
frequencies = np.linspace(10, 10000, 1000)  # 10 Hz to 10 kHz

# Plotting
plt.figure(figsize=(10, 6))
for R in resistance_values:
    noise_psd = thermal_noise_psd(R)
    resistance_label = format_resistance_label(R)
    print(f'Resistance: {resistance_label}, Thermal Noise PSD: {noise_psd} V/sqrt(Hz)')
    plt.plot(frequencies, [noise_psd] * len(frequencies), label=resistance_label)

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Thermal Noise PSD (V/$\sqrt{Hz}$)")
plt.title("Thermal Noise Power Spectral Density for Various Resistances")
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()
