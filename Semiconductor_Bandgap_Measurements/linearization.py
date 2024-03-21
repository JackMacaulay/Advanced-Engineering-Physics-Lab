# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:54:01 2024

@author: jackm
"""

import numpy as np
import pandas as pd
from scipy.constants import Boltzmann, eV
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.signal import savgol_filter
from scipy.signal import argrelextrema
csv_path = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb27_Testing/Temp_Sweep.csv"
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
#%%
# Assuming 'data' is a DataFrame with 'Temperature' (in K) and 'Resistance' (in Ohms)
data = pd.read_csv(csv_path, skiprows=1) 
# Calculate the reciprocal temperature (1/T)


min_resistance = data['Resistance'].min()

# Shift the resistance values so the minimum becomes 0
data['Adjusted Resistance'] = data['Resistance'] - min_resistance


plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature'], (data['Resistance']), color = 'black', label = 'Original Data', s = 5)
plt.scatter(data['Temperature'], data['Adjusted Resistance'], color = 'red', label = 'Adjusted resistance', s = 5)
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.title('Silicon Semiconductor Resistance vs. Temperature')
plt.legend()
plt.grid(True)
plt.show()
#%%



# Data Smoothing with Savitzky-Golay filter
# The window size and polynomial order are chosen based on the dataset's characteristics
# Window size needs to be odd, and a typical choice for polynomial order is 2 or 3
window_size = 99  # Choose an odd number
poly_order = 3

data['Smoothed Resistance'] = savgol_filter(data['Adjusted Resistance'], window_size, poly_order)

# Plotting raw vs. smoothed data for comparison
plt.figure(figsize=(12, 6))
plt.scatter(data['Temperature'], data['Adjusted Resistance'], label='Raw Data', color = 'black',alpha=0.5, s=5)
plt.scatter(data['Temperature'], data['Smoothed Resistance'], label='Smoothed Data', color='red', s = 5)
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.title('Raw vs. Smoothed Resistance Data')
plt.legend()
plt.grid(True)
plt.show()
#%%

# Calculate the first derivative of resistance with respect to temperature
data['dR/dT'] = np.gradient(data['Smoothed Resistance'], data['Temperature'])

filtered_data = data
minima_indices = argrelextrema(filtered_data['dR/dT'].values, np.less)[0]

# Extract corresponding temperatures and dR/dT values
minima_temperatures = filtered_data.iloc[minima_indices]['Temperature']
minima_values = filtered_data.iloc[minima_indices]['dR/dT']

plt.scatter(filtered_data['Temperature'], filtered_data['dR/dT'], label='dR/dT', color='black', s=5)
plt.scatter(minima_temperatures.iloc[34], minima_values.iloc[34], color='red', label='Local Minima')
plt.axvline(minima_temperatures.iloc[34])
plt.xlabel('Temperature (K)')
plt.ylabel('dR/dT')
plt.title('First Derivative of Resistance')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
print(minima_temperatures.iloc[34])

#%% First step of lineraization
# Linearize the resistance data by taking the natural log of the resistance
# Filter out rows in `data` where 'Temperature' is below the threshold
data = data[(data['Temperature'] >= 500) & (data['Temperature'] <= 630)]

plt.plot(data['Temperature'], data['Smoothed Resistance'])
plt.show()

print(len(data['Temperature']))
print(len(data['Smoothed Resistance']))
#%%
data['RT^3/2'] = data['Smoothed Resistance'] * (data['Temperature'] ** (3/2))

# Take the natural log of RT^(3/2)
data['ln(RT^3/2)'] = np.log(data['RT^3/2'])
data['1/T'] = 1 / data['Temperature']

# Perform linear regression on ln(RT^(3/2)) vs 1/T
slope, intercept, r_value, p_value, std_err = linregress(data['1/T'], data['ln(RT^3/2)'])

# Calculate the bandgap energy Eg using the slope (Eg = 2 * slope * k_B)
# Note: Boltzmann's constant (k_B) is in J/K, converting to eV by dividing by e
Eg = 2 * slope * Boltzmann / eV

print(f"Estimated Band Gap Energy: {Eg:.4f} eV")
line_eq = f'ln(RT^3/2) = {slope:.4f} × (1/T) + {intercept:.4f}'

annotation_y = intercept + slope * data['1/T'].min() + 0.4  # Adjust the 0.05 to move the annotation higher

# Plotting for visualization
plt.figure(figsize=(10, 6))
delta_T = 1  # Uncertainty in temperature, in K
delta_R = 5  # Uncertainty in resistance, in Ohms

# Calculate RT^(3/2) with its uncertainty (theoretical demonstration)
Eg = 2 * slope * Boltzmann / eV
uncertainty_Eg = 2 * std_err * Boltzmann / eV
print(f"Estimated Band Gap Energy: {Eg:.4f} eV, with uncertainty: {uncertainty_Eg:.4f} eV")

# Plotting for visualization with error bars
plt.figure(figsize=(10, 6))
# Adding error bars for both ln(RT^3/2) and 1/T using their uncertainties
plt.errorbar(data['1/T'], data['ln(RT^3/2)'], fmt='o', color='blue', label='New Temperature Range', markersize=3)
line_eq = f'ln(RT^3/2) = {slope:.4f} × (1/T) + {intercept:.4f}'
plt.plot(data['1/T'], intercept + slope * data['1/T'], 'r', label=f'Linear Fit: {line_eq}', color ='black')
plt.xlabel('1/T (1/K)')
plt.ylabel('ln(RT^3/2)')
plt.title('Linearization for Band Gap Energy Estimation')
plt.legend()
plt.grid(True)

# Annotate the linear equation
annotation_y = intercept + slope * data['1/T'].min() + 0.4  # Adjust the position to move the annotation


plt.show()

# Print the fit parameters
print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"Correlation Coefficient (r_value): {r_value}")
print(f"P-value: {p_value}")
print(f"Standard Error: {std_err}")
experimental_value = 1.0629
theoretical_value = 1.16978
experimental_uncertainty = 0.0157
percent_difference = (abs(experimental_value - theoretical_value) / theoretical_value) * 100
percent_uncertainty = (experimental_uncertainty / experimental_value) * 100

print(percent_difference)
print(percent_uncertainty)

