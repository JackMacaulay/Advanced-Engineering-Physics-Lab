import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.cm as cm
from scipy.stats import linregress

plt.style.use('seaborn-whitegrid')  # Set a clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 

# Getting the differential data and cleaning it up
parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
csv_files_directory = os.path.join(parent_directory, 'Good_Cryo_Data')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

# Add the 'Feb_06_405_Cold_Diff.csv' file back to the list
csv_files.append('Feb_06_405_Cold_Diff.csv')

dataframes = {}

# Loop through each CSV file and create a DataFrame
for file in csv_files:
    file_path = os.path.join(csv_files_directory, file)
    # Read the CSV file and skip the first row (header) using skiprows=1
    data = pd.read_csv(file_path, skiprows=1, names=['Frequency', '998 kohm'])
    # Store the DataFrame in the dictionary with the file name as the key
    dataframes[file] = data

# Constants for theoretical calculations
k = 1.38e-23  # Boltzmann's constant in J/K
T = 170  # Convert temperature from Celsius to Kelvin

# Get the DataFrame for the experimental results of the 998 kohm resistor
experimental_df = dataframes['Feb_06_405_Cold_Diff.csv']

# Define the color for both experimental and theoretical lines
color_both = cm.tab10(0)  # Choose a color from tab10 colormap

def thermal_noise_psd(R):
    return np.sqrt(4 * k * T * R)

# Plotting
plt.figure(figsize=(10, 6))
min_freq = 190
max_freq = 2000
plt.axvline(x=min_freq, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=max_freq, color='gray', linestyle='--', linewidth=1)

plt.text(min_freq, 0.000001, f'{min_freq} Hz', rotation=90, verticalalignment='bottom')
plt.text(max_freq, 0.000001, f'{max_freq} Hz', rotation=90, verticalalignment='bottom')


# Plot experimental data
plt.plot(experimental_df['Frequency'], experimental_df['998 kohm'], label='Experimental', color=color_both, marker='o')

# Plot theoretical data
theoretical_psd = thermal_noise_psd(998e3)  # Calculate theoretical PSD for 998 kohm resistor
plt.plot(experimental_df['Frequency'], [theoretical_psd] * len(experimental_df), label='Theoretical', linestyle='--', color=color_both)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Experimental vs Theoretical Noise, Cryostat (998 kΩ, T ≈ 170 K)")
plt.legend()

plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.show()
combined_dataframe = dataframes
frequency_values = experimental_df['Frequency']
#%%zoomed in
# Calculate theoretical thermal noise PSD uncertainty for each resistor
std_noise_values = {}
for file, df in dataframes.items():
    resistor_value = file.split('_')[2].split('.')[0]  # Extract resistor value from filename
    Delta_R = 0.01 * float(resistor_value)  # 1% uncertainty in resistance
    
    # Theoretical thermal noise PSD uncertainty
    Delta_S_v = np.sqrt((4 * k * T * Delta_R)**2)
    
    # Calculate standard deviation of noise measurements within the frequency range
    noise_measurements = df['998 kohm'][(df['Frequency'] >= 190) & (df['Frequency'] <= 2000)]
    std_noise_measurement = np.std(noise_measurements, ddof=1)  # ddof=1 for sample standard deviation
    
    # Combine uncertainties
    total_uncertainty = np.sqrt(Delta_S_v**2 + std_noise_measurement**2)
    
    std_noise_values[file] = total_uncertainty

# Print the calculated uncertainties for each file (resistor)
for file, uncertainty in std_noise_values.items():
    print(f"Total uncertainty for {file}: {uncertainty:.2e} V/sqrt(Hz)")

#%%
plt.figure(figsize=(10, 6))

# Choose a color for both experimental and theoretical lines
color_998 = 'blue'  # Manually set color for 998 kΩ resistor

# Filter the dataframe for the 998 kΩ resistor
df_998 = dataframes['Feb_06_405_Cold_Diff.csv']

# Filter the dataframe to include only the specified frequency range
filtered_df_998 = df_998[(df_998['Frequency'] >= 190) & (df_998['Frequency'] <= 2000)]

# Calculate theoretical thermal noise PSD for the 998 kΩ resistor
theoretical_psd_998 = thermal_noise_psd(998e3)

# Plot experimental data with error bars
plt.errorbar(filtered_df_998['Frequency'], filtered_df_998['998 kohm'], yerr=std_noise_values['Feb_06_405_Cold_Diff.csv'], label='Experimental 998 kΩ', fmt='o', markersize=3, ecolor='lightgray', elinewidth=3, capsize=0)

# Plot theoretical data
plt.plot(filtered_df_998['Frequency'], [theoretical_psd_998] * len(filtered_df_998), label='Theoretical 998 kΩ', linestyle='--', color=color_998)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Experimental and Theoretical Noise vs. Frequency (190 Hz to 2000 Hz) for Cryostat")
plt.legend()
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.show()

#%%

# Define the frequency range for calculation
min_freq_range = 190
max_freq_range = 2000

# Filter the noise measurements within the specified frequency range
filtered_noise_measurements = experimental_df['998 kohm'][(experimental_df['Frequency'] >= min_freq_range) & (experimental_df['Frequency'] <= max_freq_range)]

# Calculate the average noise within the frequency range
average_noise = np.mean(filtered_noise_measurements)

# Calculate the uncertainty in the average noise (standard error of the mean, SEM)
sem_noise = np.std(filtered_noise_measurements, ddof=1) / np.sqrt(len(filtered_noise_measurements))

# Print the average noise and uncertainty
print(f"Average noise within {min_freq_range} Hz to {max_freq_range} Hz: {average_noise:.2e} V/sqrt(Hz)")
print(f"Uncertainty in the average noise: {sem_noise:.2e} V/sqrt(Hz)")

# Calculate theoretical thermal noise PSD for the 998 kΩ resistor within the specified frequency range
theoretical_psd_998_within_range = thermal_noise_psd(998e3)

# Print the theoretical value
print(f"Theoretical noise within {min_freq_range} Hz to {max_freq_range} Hz: {theoretical_psd_998_within_range:.2e} V/sqrt(Hz)")

# Calculate percent error
percent_error = ((average_noise - theoretical_psd_998_within_range) / theoretical_psd_998_within_range) * 100

# Print percent error
print(f"Percent error compared to theoretical value: {percent_error:.2f}%")
