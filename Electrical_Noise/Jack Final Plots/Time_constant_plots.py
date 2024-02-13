import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 1000}) 

# Get the parent directory of the current directory
parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Define the directory containing CSV files
csv_files_directory = os.path.join(parent_directory, 'TimeConstant_Sweep')

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_dataframe = pd.DataFrame()

# Loop through each CSV file and append the data to the combined DataFrame
for file in csv_files:
    # Extract time constant from file name using regular expression
    time_constant_match = re.search(r'(?<=_)\d+(?=ms)', file)  # Extracts digits followed by 'ms' preceded by '_'
    time_constant_value = int(time_constant_match.group()) if time_constant_match else None
    
    # Read CSV file into a DataFrame
    file_path = os.path.join(csv_files_directory, file)
    data = pd.read_csv(file_path, sep=',', names=['Frequency', 'Noise'])
    
    # Set time constant as the column header
    data.columns = ['Frequency', time_constant_value]
    
    # Append data to the combined DataFrame
    combined_dataframe = pd.concat([combined_dataframe, data.iloc[1:]], axis=1)

# Reset the index
combined_dataframe.reset_index(drop=True, inplace=True)
combined_dataframe = combined_dataframe.apply(pd.to_numeric, errors='coerce')

# Drop additional frequency columns
combined_dataframe = combined_dataframe.loc[:, ~combined_dataframe.columns.duplicated()]

plt.figure(figsize=(10, 6))
for column in combined_dataframe.columns[1:]:
    plt.plot(combined_dataframe['Frequency'], combined_dataframe[column], label=f"{column} ms")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Noise (V/$\sqrt{\mathrm{Hz}}$)")
plt.xscale('log')
plt.yscale('log')
plt.title("Noise Spectrum for 50 $\Omega$ Terminator with Different Time Constants")
plt.legend(title='Time Constant', loc='upper right')
plt.grid(True)

# Format tick labels to display in µV or nV
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.tight_layout()  # Adjust layout to prevent cropping
plt.show()
