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
csv_files_directory = os.path.join(parent_directory, 'Jan_30_Clean_Data')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

dataframes = {}

# Specify the resistor values directly, excluding the 50 Ohm data
resistance_values = [1492.5e3, 250e3, 50, 510e3, 998e3]

# Sort the CSV files to match the resistor values and exclude the 50 Ohm data
sorted_csv_files = sorted([f for f in csv_files if f.endswith('.csv') and not f.startswith('50')])

# Check if the number of sorted files matches the number of resistor values
if len(sorted_csv_files) != len(resistance_values):
    raise ValueError("The number of sorted CSV files does not match the number of resistor values provided.")

# Loop through each CSV file and map it to a resistor value
for file, resistor_value in zip(sorted_csv_files, resistance_values):
    file_path = os.path.join(csv_files_directory, file)
    data = pd.read_csv(file_path, sep=',', names=['Frequency', 'Noise'])

    # Store the DataFrame in the dictionary with the resistor value as the key
    dataframes[str(resistor_value)] = data

#%%
# Remove the headers from all dataframes
for resistor_value, dataframe in dataframes.items():
    if resistor_value != '50':
        dataframes[resistor_value] = dataframe.drop(0)

# Combine all dataframes into one dataframe with just the 'Frequency' column initially
combined_dataframe = dataframes[list(dataframes.keys())[0]][['Frequency']]

# Iterate through the dataframes and append the 'Noise' columns
for resistor_value, dataframe in dataframes.items():
    if resistor_value != '50':
        combined_dataframe[resistor_value + ' Ohms'] = dataframe['Noise'].values

# Reset the index of the combined dataframe and convert all columns to numeric
combined_dataframe.reset_index(drop=True, inplace=True)
combined_dataframe = combined_dataframe.apply(pd.to_numeric, errors='coerce')


# Constants for theoretical calculations
k = 1.38e-23  # Boltzmann's constant in J/K
T = 22.5 + 273.15  # Convert temperature from Celsius to Kelvin

def thermal_noise_psd(R):
    return np.sqrt(4 * k * T * R)

frequency_values = combined_dataframe['Frequency'].values
resistance_values = [value for value in resistance_values if value != 50]
print(combined_dataframe.columns)
#%% Plotting
plt.figure(figsize=(10, 6))

# Define a list of colors for the plots
colors = cm.tab10(np.linspace(0, 1, len(resistance_values)))

# Plot experimental data
# Plot experimental data
for i, (resistor_value, color) in enumerate(zip(combined_dataframe.columns[1:], colors)):
    R_value = float(resistor_value.split()[0])  # Extract the numeric resistor value from the column name
    label = f'{R_value / 1e3:.0f} kΩ' if R_value >= 1e3 else f'{R_value:.0f} Ω'
    plt.plot(frequency_values, combined_dataframe[resistor_value], label=label, linewidth=2, color=color, marker = 'o')

# Plot theoretical data
for i, R in enumerate(resistance_values):
    noise_psd = thermal_noise_psd(R)
    label = f'Theoretical {R / 1e3:.0f} kΩ' if R >= 1e3 else f'Theoretical {R:.0f} Ω'
    # Use the same color for the theoretical line as the experimental data
    plt.plot(frequency_values, [noise_psd]*len(frequency_values), label=label, linewidth=2, linestyle='--', color=colors[i])
min_freq = 190
max_freq = 1500
plt.axvline(x=min_freq, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=max_freq, color='gray', linestyle='--', linewidth=1)

plt.text(min_freq, 0.000001, f'{min_freq} Hz', rotation=90, verticalalignment='bottom')
plt.text(max_freq, 0.000001, f'{max_freq} Hz', rotation=90, verticalalignment='bottom')


plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Single-Ended Noise Measurements for Different Resistors")
plt.legend(title="Resistor Value", loc='upper right', ncol=2)  # Adjust legend columns for better readability
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.show()

#%% Noise calculations
T_Celsius = 22.5  # Temperature in Celsius
T = T_Celsius + 273.15  # Convert temperature to Kelvin
Delta_T = 0.1  # Uncertainty in temperature in Kelvin

# Calculate theoretical thermal noise PSD uncertainty for each resistor
std_noise_values = {}
for resistor_value in resistance_values:
    Delta_R = 0.01 * resistor_value  # 1% uncertainty in resistance
    # Theoretical thermal noise PSD uncertainty
    Delta_S_v = np.sqrt((4 * k * T * Delta_R)**2 + (4 * k * resistor_value * Delta_T)**2)
    
    # Calculate standard deviation of noise measurements within the frequency range
    noise_measurements = combined_dataframe[str(resistor_value) + ' Ohms'][(frequency_values >= 190) & (frequency_values <= 1500)]
    std_noise_measurement = np.std(noise_measurements, ddof=1)  # ddof=1 for sample standard deviation
    
    # Combine uncertainties
    total_uncertainty = np.sqrt(Delta_S_v**2 + std_noise_measurement**2)
    
    std_noise_values[str(resistor_value) + ' Ohms'] = total_uncertainty

# Print the calculated uncertainties for each resistor
for resistor, uncertainty in std_noise_values.items():
    print(f"Total uncertainty for {resistor}: {uncertainty:.2e} V/sqrt(Hz)")

#%% Filtered Plot

# Filter the frequency values
filtered_frequency_values = frequency_values[(frequency_values >= 190) & (frequency_values <= 1500)]

plt.figure(figsize=(10, 6))
# Plot experimental data with filtered noise values
for i, (resistor_value, color) in enumerate(zip(combined_dataframe.columns[1:], colors)):
    R_value = float(resistor_value.split()[0])  # Extract the numeric resistor value from the column name
    label = f'{R_value / 1e3:.0f} kΩ' if R_value >= 1e3 else f'{R_value:.0f} Ω'
    filtered_noise_values = combined_dataframe[resistor_value][(frequency_values >= 190) & (frequency_values <= 1500)]
    std_noise = std_noise_values[resistor_value]  # Assuming you have a dictionary of standard deviations
    plt.plot(filtered_frequency_values, filtered_noise_values, color=color, linestyle='-', marker='o', label=label)

    # Plot with error bars
    plt.errorbar(filtered_frequency_values, filtered_noise_values, yerr=std_noise, fmt='o', color=color, ecolor='lightgray', elinewidth=3, capsize=0)


# Plot theoretical data with matching colors
for i, R in enumerate(resistance_values):
    noise_psd = thermal_noise_psd(R)
    label = f'Theoretical {R / 1e3:.0f} kΩ' if R >= 1e3 else f'Theoretical {R:.0f} Ω'
    plt.plot(filtered_frequency_values, [noise_psd] * len(filtered_frequency_values), label=label, linewidth=2, linestyle='--', color=colors[i])

plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise(V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Experimental and Theoretical Thermal Noise (190 Hz to 1500 Hz)")
# Move the legend outside the plot and adjust its position
plt.legend(title="Resistor Value", loc='upper left', bbox_to_anchor=(1.02, 1), ncol=1)
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.show()


#%%Determining Boltzmann's constant


# Calculate the average noise squared and its uncertainty for each resistor
average_noise_squared_and_uncertainty = {}

for resistor_value in combined_dataframe.columns[1:]:
    # Filter the noise values for the frequency band
    filtered_noise_values = combined_dataframe[resistor_value][(combined_dataframe['Frequency'] >= 190) & (combined_dataframe['Frequency'] <= 1500)]
    avg_noise = np.mean(filtered_noise_values)
    avg_noise_squared = avg_noise ** 2
    std_dev_noise = np.std(filtered_noise_values, ddof=1)  # Calculate standard deviation
    # Number of measurements
    N = len(filtered_noise_values)
    # Standard error of the mean
    sem_noise = std_dev_noise / np.sqrt(N)
    # Error propagation for the average noise squared
    error_avg_noise_squared = 2 * avg_noise * sem_noise
    # Store in the dictionary
    average_noise_squared_and_uncertainty[str(resistor_value)] = (avg_noise_squared, error_avg_noise_squared)

# ... [additional code] ...

# Extract the average noise squared values and their uncertainties
avg_noise_squared_values = [val[0] for val in average_noise_squared_and_uncertainty.values()]
avg_noise_squared_uncertainties = [val[1] for val in average_noise_squared_and_uncertainty.values()]

# Calculate the 1% resistance uncertainties for the x-axis
resistance_uncertainties = [0.01 * R for R in resistance_values]


plt.figure(figsize=(10, 6))
# Plot the average noise squared with error bars
plt.errorbar(resistance_values, avg_noise_squared_values, xerr=resistance_uncertainties, yerr=avg_noise_squared_uncertainties, fmt='o', color='black', label='Average Noise Squared', ecolor='red', elinewidth=3, capsize=0)

# Perform linear regression
# Calculate Boltzmann's constant
slope, intercept, r_value, p_value, std_err = linregress(resistance_values, avg_noise_squared_values)

# Create the linear regression line
linear_fit = slope * np.array(resistance_values) + intercept
noise = 'noise'
equation_text = f'Linear Fit: $V_{{{noise}}}^2 = {slope:.2e} \\cdot R + {intercept:.2e}$'

# Plot the linear regression line
plt.plot(resistance_values, linear_fit, color='blue', label = equation_text)

plt.legend()
plt.title("Single-Ended Average Noise Squared Vs Resistance", y = 1.05)
plt.xlabel("Resistance ($\Omega$)")
plt.ylabel("Noise Squared ($V^2$/${\mathrm{Hz}}$)")
plt.tight_layout()
plt.show()

actual_boltzmann_constant = 1.38e-23  # Actual Boltzmann's constant value
calculated_slope = slope/(4 * T)  # Your calculated slope

# The error in the slope from the linear regression is std_err
# The propagated error in Boltzmann's constant is given by:
boltzmann_constant_error = std_err / (4 * T)

# Calculate the calculated Boltzmann's constant and its percent error, including the propagated error
calculated_slope = slope / (4 * T)
calculated_slope_error = boltzmann_constant_error

# Calculate percent error
percent_error = np.abs((calculated_slope - actual_boltzmann_constant) / actual_boltzmann_constant) * 100
percent_error_in_slope = (calculated_slope_error / calculated_slope) * 100

#%%
average_noise_bandwidth = {}
average_noise_bandwidth_uncertainty = {}

for resistor_value in resistance_values:
    noise_data = combined_dataframe[str(resistor_value) + ' Ohms'][(combined_dataframe['Frequency'] >= min_freq) & (combined_dataframe['Frequency'] <= max_freq)]
    average_noise = np.mean(noise_data)
    std_dev_noise = np.std(noise_data, ddof=1)
    N = len(noise_data)
    sem_noise = std_dev_noise / np.sqrt(N)
    average_noise_bandwidth[str(resistor_value)] = average_noise
    average_noise_bandwidth_uncertainty[str(resistor_value)] = sem_noise

# Print the average noise reading over the limited bandwidth with the uncertainty
for resistor_value in sorted(resistance_values):
    average_noise = average_noise_bandwidth[str(resistor_value)]
    uncertainty = average_noise_bandwidth_uncertainty[str(resistor_value)]
    theoretical_noise = thermal_noise_psd(resistor_value)
    print(f"Resistor {resistor_value / 1e3:.0f} kΩ: Average Noise = {average_noise:.2e} V/sqrt(Hz) ± {uncertainty:.2e}, Theoretical = {theoretical_noise:.2e} V/sqrt(Hz)")
