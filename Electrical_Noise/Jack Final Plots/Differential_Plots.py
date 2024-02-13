import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.cm as cm
from scipy.stats import linregress

plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 

#%% Getting the differential data and cleaning it up

parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
csv_files_directory = os.path.join(parent_directory, 'Differential')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

# Initialize an empty dictionary to store DataFrames
dataframes = {}

# Loop through each CSV file and create a DataFrame with the title as the resistance value
for file in csv_files:
    resistor_value = file.split('_')[3]
    file_path = os.path.join(csv_files_directory, file)
    data = pd.read_csv(file_path, sep=',', names=['Frequency', 'Noise'])
    dataframes[resistor_value] = data

# Remove the headers from all three dataframes
for resistor_value, dataframe in dataframes.items():
    dataframes[resistor_value] = dataframe.drop(0)
# Combine all dataframes into one dataframe
# Initialize an empty dataframe with just the 'Frequency' column
combined_dataframe = dataframes[list(dataframes.keys())[0]][['Frequency']]

# Iterate through the dataframes and append the 'Noise' columns
for resistor_value, dataframe in dataframes.items():
    if resistor_value != '50':
        combined_dataframe[resistor_value + ' Ohms'] = dataframe['Noise'].values

# Reset the index
combined_dataframe.reset_index(drop=True, inplace=True)
combined_dataframe = combined_dataframe.apply(pd.to_numeric, errors='coerce')
headers = ['Frequency', '1492500.0 Ohms', '250000.0 Ohms', '510000.0 Ohms', '998000.0 Ohms']

# Set the headers of the combined_dataframe
combined_dataframe.columns = headers
print(combined_dataframe)
#%% Calculating theoretical stuff
# Constants
k = 1.38e-23  # Boltzmann's constant in J/K
T = 22.5 + 273.15  # Convert temperature from Celsius to Kelvin

# Resistance values for specific comparison points
special_resistances = [1492.5e3, 250e3, 510e3, 0.998e6]  # Omitting the 50 ohm value for clarity


def thermal_noise_psd(R):
    return np.sqrt(4 * k * T * R)

def thermal_noise_psd_squared(R, k_fit):
    return 4 * k_fit * T * R

frequency_values = combined_dataframe['Frequency'].values

print(combined_dataframe)

#%%Plotting
plt.figure(figsize=(10, 6))
colors = cm.tab10(np.linspace(0, 1, len(special_resistances)))

# Iterate through the combined_dataframe columns and special_resistances with corresponding colors
for i, (resistor_value, color) in enumerate(zip(combined_dataframe.columns[1:], colors)):
    formatted_resistor_value = f'{resistor_value.split("KOhm")[0]} K$\\Omega$'
    plt.plot(frequency_values, combined_dataframe[resistor_value], label=formatted_resistor_value, linewidth=2, color=color, marker ='o')

for i, R in enumerate(special_resistances):
    noise_psd = thermal_noise_psd(R)
    label = f'Theoretical {R / 1e3:.0f} kΩ' if R >= 1e3 else f'Theoretical {R:.0f} Ω'
    theoretical_color = colors[i % len(colors)]  # Reuse the same colors from the list
    plt.plot(frequency_values, [noise_psd]*len(frequency_values), label=label, linewidth=2, linestyle='--', color=theoretical_color)

min_freq = 190
max_freq = 2000
plt.axvline(x=min_freq, color='gray', linestyle='--', linewidth=1)
plt.axvline(x=max_freq, color='gray', linestyle='--', linewidth=1)
plt.text(min_freq, 0.000001, f'{min_freq} Hz', rotation=90, verticalalignment='bottom')
plt.text(max_freq, 0.000001, f'{max_freq} Hz', rotation=90, verticalalignment='bottom')


plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Differential Noise Measurements for Different Resistors")
plt.legend(title="Resistor Value")
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
for resistor_value in special_resistances:
    Delta_R = 0.01 * resistor_value  # 1% uncertainty in resistance
    # Theoretical thermal noise PSD uncertainty
    Delta_S_v = np.sqrt((4 * k * T * Delta_R)**2 + (4 * k * resistor_value * Delta_T)**2)
    
    # Calculate standard deviation of noise measurements within the frequency range
    noise_measurements = combined_dataframe[str(resistor_value) + ' Ohms'][(frequency_values >= 190) & (frequency_values <= 2000)]
    std_noise_measurement = np.std(noise_measurements, ddof=1)  # ddof=1 for sample standard deviation
    
    # Combine uncertainties
    total_uncertainty = np.sqrt(Delta_S_v**2 + std_noise_measurement**2)
    
    std_noise_values[str(resistor_value) + ' Ohms'] = total_uncertainty

# Print the calculated uncertainties for each resistor
for resistor, uncertainty in std_noise_values.items():
    print(f"Total uncertainty for {resistor}: {uncertainty:.2e} V/sqrt(Hz)")


#%% Filtered Plot

# Filter the frequency values
filtered_frequency_values = frequency_values[(frequency_values >= 190) & (frequency_values <= 2000)]

plt.figure(figsize=(10, 6))


# Iterate through the combined_dataframe columns and special_resistances with corresponding colors
for i, (resistor_value, color) in enumerate(zip(combined_dataframe.columns[1:], colors)):
    R_value = float(resistor_value.split()[0])  # Extract the numeric resistor value from the column name
    label = f'{R_value / 1e3:.0f} kΩ' if R_value >= 1e3 else f'{R_value:.0f} Ω'
    # Filter the noise values based on the filtered frequency values
    filtered_noise_values = combined_dataframe[resistor_value][(frequency_values >= 190) & (frequency_values <= 2000)]
    std_noise = std_noise_values[resistor_value]  # Assuming you have a dictionary of standard deviations
    plt.plot(filtered_frequency_values, filtered_noise_values, color=color, linestyle='-', marker='o', label=label)

    # Plot with error bars
    plt.errorbar(filtered_frequency_values, filtered_noise_values, yerr=std_noise, fmt='o', color=color, ecolor='lightgray', elinewidth=3, capsize=0)

for i, R in enumerate(special_resistances):
    noise_psd = thermal_noise_psd(R)
    label = f'Theoretical {R / 1e3:.0f} kΩ' if R >= 1e3 else f'Theoretical {R:.0f} Ω'
    theoretical_color = colors[i % len(colors)]  # Reuse the same colors from the list
    # Plot the theoretical noise values only for the filtered frequency values
    plt.plot(filtered_frequency_values, [noise_psd] * len(filtered_frequency_values), label=label, linewidth=2, linestyle='--', color=theoretical_color)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
plt.title("Experimental and Theoretical Thermal Noise vs. Frequency (190 Hz to 2000 Hz)")
plt.legend(title="Resistor Value", loc='upper left', bbox_to_anchor=(1.02, 1), ncol=1)
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.show()

#%%

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
resistance_values = special_resistances
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
plt.title("Differential Average Noise Squared Vs Resistance", y = 1.05)
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
actual_boltzmann_constant = 1.38e-23

# Calculate the experimental Boltzmann's constant
experimental_boltzmann_constant = calculated_slope

# Calculate the uncertainty in the experimental Boltzmann's constant
experimental_boltzmann_constant_uncertainty = calculated_slope_error

# Calculate the percent error
percent_error = np.abs((experimental_boltzmann_constant - actual_boltzmann_constant) / actual_boltzmann_constant) * 100

# Calculate the uncertainty in the percent error
percent_error_uncertainty = (percent_error / experimental_boltzmann_constant) * experimental_boltzmann_constant_uncertainty

# Print the experimental Boltzmann's constant and its uncertainty
print(f"Experimental Boltzmann's constant: {experimental_boltzmann_constant:.2e} J/K ± {experimental_boltzmann_constant_uncertainty:.2e} J/K")

# Print the percent error and its uncertainty
print(f"Percent error: {percent_error:.2f}% ± {percent_error_uncertainty:.2f}%")
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
