import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 1000}) 
# Get the parent directory of the current directory
parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Define the directory containing CSV files
csv_files_directory = os.path.join(parent_directory, 'Terminator_Sweep')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_dataframe = pd.DataFrame()

# Loop through each CSV file and append the data to the combined DataFrame
for file in csv_files:
    # Extract impedance and material from file name
    impedance_str, material = file.split('_')[-2], file.split('_')[-1].split('.')[0]
    # Format impedance
    impedance = f"{impedance_str} $\\Omega$"  # Format impedance with omega symbol
    
    # Remove the word 'ohm' from the impedance label
    impedance = impedance.replace('ohm', '$\\Omega$')
    
    # Read CSV file into a DataFrame
    file_path = os.path.join(csv_files_directory, file)
    data = pd.read_csv(file_path, sep=',', names=['Frequency', 'Noise'])
    
    # Set impedance and material as the column header
    column_label = f"{impedance} {material.capitalize()}"
    data.columns = ['Frequency', column_label]
    
    # Append data to the combined DataFrame
    combined_dataframe = pd.concat([combined_dataframe, data.iloc[1:]], axis=1)

# Reset the index
combined_dataframe.reset_index(drop=True, inplace=True)
combined_dataframe = combined_dataframe.apply(pd.to_numeric, errors='coerce')

# Drop additional frequency columns
combined_dataframe = combined_dataframe.loc[:, ~combined_dataframe.columns.duplicated()]

plt.figure(figsize=(10, 6))
for column in combined_dataframe.columns[1:]:
    plt.plot(combined_dataframe['Frequency'], combined_dataframe[column], label=column)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\\sqrt{\\mathrm{Hz}}$)")
plt.xscale('log')
plt.yscale('log')
plt.title("Noise Spectrum for Different Terminators")
plt.legend(title='Material and Impedance')
plt.grid(True)

# Format tick labels to display in µV or nV
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.tight_layout()  # Adjust layout to prevent cropping
plt.show()
