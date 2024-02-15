import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
# Path to the CSV file
file_path = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb13_Testing/Wafer_Test_Constant_Temp.csv"
file_path_2 = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb13_Testing/Wafer_Test_Temp.csv"

# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data = pd.read_csv(file_path, skiprows=1, header=None, names=['Temperature', 'Resistance'])
data[['Temperature', 'Resistance']] = data['Temperature'].str.split(',', expand=True)

# Remove any non-numeric rows and convert columns to numeric types
data = data[data['Temperature'].apply(lambda x: x.replace('.', '', 1).isdigit())]
data['Temperature'] = pd.to_numeric(data['Temperature'])
data['Resistance'] = pd.to_numeric(data['Resistance'])

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature'], data['Resistance'], color='blue', alpha=0.5)
plt.title('Resistance vs. Temperature for Fixed T')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.grid(True)
plt.show()


#%% Average resistance from no temp change
average_resistance = data['Resistance'].mean()

# Print the average resistance
print("Average Resistance:", average_resistance)

#%% Plotting data with changing temp
# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data = pd.read_csv(file_path_2, skiprows=1, header=None, names=['Temperature', 'Resistance'])
data[['Temperature', 'Resistance']] = data['Temperature'].str.split(',', expand=True)

# Remove any non-numeric rows and convert columns to numeric types
data = data[data['Temperature'].apply(lambda x: x.replace('.', '', 1).isdigit())]
data['Temperature'] = pd.to_numeric(data['Temperature'])
data['Resistance'] = pd.to_numeric(data['Resistance'])

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature'], data['Resistance'], color='blue', alpha=0.5)
plt.title('Resistance vs. Temperature')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.grid(True)
plt.show()

#%%
plt.figure(figsize=(10, 6))
plt.scatter(1/data['Temperature'], np.log10(data['Resistance']), color='blue', alpha=0.5)
plt.title('Resistance vs. Temperature')
plt.xlabel('1/Temperature (1/K)')
plt.ylabel('ln(Resistance)')
plt.grid(True)
plt.show()