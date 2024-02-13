import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import hsv_to_rgb

plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 1000}) 

# Get the parent directory of the current directory
parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Define the directory containing CSV files
csv_files_directory = os.path.join(parent_directory, 'Jan_25_Sensitivity_Sweep')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_dataframe = pd.DataFrame()

# Loop through each CSV file and append the data to the combined DataFrame
for i, file in enumerate(csv_files):
    # Extract sensitivity from file name
    sensitivity_str = file.split('_')[-1].split('.')[0]
    # Remove the unit from sensitivity_str
    sensitivity_value = float(sensitivity_str[:-2])  # Remove the last two characters (the unit)
    # Check the unit and convert sensitivity to volts accordingly
    if sensitivity_str.endswith('nV'):
        sensitivity = sensitivity_value * 1e-9  # Convert nV to V
    elif sensitivity_str.endswith('uV'):
        sensitivity = sensitivity_value * 1e-6  # Convert µV to V
    else:
        raise ValueError("Invalid sensitivity unit. Sensitivity must be in nV or µV.")
    
    # Read CSV file into a DataFrame
    file_path = os.path.join(csv_files_directory, file)
    data = pd.read_csv(file_path, sep=',', names=['Frequency', 'Noise'])
    
    # Set sensitivity as the column header
    data.columns = ['Frequency', sensitivity]
    
    # Append data to the combined DataFrame
    combined_dataframe = pd.concat([combined_dataframe, data.iloc[1:]], axis=1)

# Reset the index
combined_dataframe.reset_index(drop=True, inplace=True)
combined_dataframe = combined_dataframe.apply(pd.to_numeric, errors='coerce')
# Drop additional frequency columns except for the first one
combined_dataframe = combined_dataframe.loc[:, ~combined_dataframe.columns.duplicated()]

# Extract and sort the column headers excluding 'Frequency'
sorted_columns = sorted(combined_dataframe.columns[1:])

# Concatenate 'Frequency' with the sorted column headers
new_columns = ['Frequency'] + sorted_columns

# Update the DataFrame columns
combined_dataframe.columns = new_columns

# Plotting the main figure
fig, ax = plt.subplots(figsize=(10, 6))
colors = [hsv_to_rgb((i/len(combined_dataframe.columns[1:]), 0.8, 0.8)) for i in range(len(combined_dataframe.columns[1:]))]
for i, column in enumerate(combined_dataframe.columns[1:]):
    # Check if the sensitivity value is smaller than 1e-6 (nanovolts)
    if abs(column) < 1e-6:
        ax.plot(combined_dataframe['Frequency'], combined_dataframe[column], label=f"{column * 1e9:.0f} nV", color=colors[i])
    else:
        ax.plot(combined_dataframe['Frequency'], combined_dataframe[column], label=f"{column * 1e6:.0f} µV", color=colors[i])

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title("Noise Spectrum for 50 $\Omega$ Terminator with Varying Sensitivity")
ax.legend(title='Sensitivity')
ax.grid(True)

# Format tick labels to display in µV or nV
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

# Adding the inset axes for zoomed-in region
axins = inset_axes(ax, width="22%", height="22%", loc='center')
for i, column in enumerate(combined_dataframe.columns[1:]):
    if abs(column) < 1e-6:
        axins.plot(combined_dataframe['Frequency'], combined_dataframe[column], label=f"{column * 1e9:.0f} nV", color=colors[i])
    else:
        axins.plot(combined_dataframe['Frequency'], combined_dataframe[column], label=f"{column * 1e6:.0f} µV", color=colors[i])

axins.set_xscale('log')
axins.set_yscale('log')
axins.set_title("Linear Region", y=1.0)  # Adjust the y parameter to move the title upwards
axins.set_xlim(250, 1e4)  # Set the limits for the zoomed-in region
axins.set_ylim(1e-9, 1e-7)
ax
