import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Enhance plot aesthetics
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 2000})  # Adjust font size and figure resolution

# Constants
k = 1.38e-23  # Boltzmann's constant in J/K
T = 22.5 + 273.15  # Convert temperature from Celsius to Kelvin

# Resistance values for specific comparison points
special_resistances = [0.998e6, 510e3, 250e3, 1.4981e6]  # Omitting the 50 ohm value for clarity
resistance_values = np.linspace(0, 2.5e6, 500)  # Smoothly varying resistance values for plotting

# Calculate thermal noise PSD
def thermal_noise_psd(R):
    return np.sqrt(4 * k * T * R)

# Format resistance labels for readability
def format_resistance_label(R):
   # if R >= 1e6:
   #     return f'{R/1e6:.1f} MΩ'
    if R >= 1e3:
        return f'{R/1e3:.0f} kΩ'
    return f'{R:.0f} Ω'

# Plot thermal noise PSD across frequencies for specific resistances
plt.figure(figsize=(8, 5))
for R in special_resistances:
    noise_psd = thermal_noise_psd(R)
    plt.plot(resistance_values, [noise_psd] * len(resistance_values), label=format_resistance_label(R), linewidth=2)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Thermal Noise PSD (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Theoretical Thermal Noise for Different Resistances")
plt.legend(title="Resistance")
plt.tight_layout()
plt.show()

#%%
# Plot thermal noise PSD vs. resistance
plt.figure(figsize=(8, 5))
noise_psd_values = [thermal_noise_psd(R) for R in resistance_values]
plt.plot(resistance_values, noise_psd_values, color='black', linewidth=2.5)

# Highlight special resistance values
#for R in special_resistances:
#    plt.plot(R, thermal_noise_psd(R), 'o', markersize=8, label=format_resistance_label(R))

plt.xlabel("Resistance (Ω)")
plt.ylabel("Theoretical Therma (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Thermal Noise PSD vs. Resistance")
#plt.legend(title="Special Resistances")
plt.tight_layout()
plt.show()

# Linear fit to determine Boltzmann's constant
def thermal_noise_psd_squared(R, k_fit):
    return 4 * k_fit * T * R

popt, _ = curve_fit(thermal_noise_psd_squared, resistance_values, np.square(noise_psd_values))
k_fit = popt[0]

# Plot PSD^2 vs. resistance with linear fit
plt.figure(figsize=(8, 5))
plt.scatter(resistance_values, np.square(noise_psd_values), color='lightgray', s=10, alpha=0.7, label='Data Points')
plt.plot(resistance_values, thermal_noise_psd_squared(resistance_values, k_fit), color='crimson', linestyle='--', linewidth=2, label='Linear Fit')

plt.xlabel("Resistance (Ω)")
plt.ylabel("Thermal Noise PSD$^2$ (V$^2$/Hz)")
plt.title("Fit to Determine Boltzmann's Constant")
plt.legend()
plt.tight_layout()
plt.show()

print(f"Fitted Boltzmann's constant: {k_fit:.2e} J/K")
