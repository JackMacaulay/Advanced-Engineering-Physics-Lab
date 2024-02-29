import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
# Path to the CSV file
csv_path = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb27_Testing/Temp_Sweep.csv"
#csv_path_2 = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb27_Testing/Temp_Sweep_2.csv"


# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data_csv = pd.read_csv(csv_path, delimiter=',', skiprows=1, header=None, names=['Temperature', 'Resistance'])
#data_csv_2 = pd.read_csv(csv_path_2, delimiter=',', skiprows=1, header=None, names=['Temperature', 'Resistance'])


# Convert 'Temperature' and 'Resistance' to numeric types if not already
data_csv['Temperature'] = pd.to_numeric(data_csv['Temperature'], errors='coerce')
data_csv['Resistance'] = pd.to_numeric(data_csv['Resistance'], errors='coerce')

#data_csv_2['Temperature'] = pd.to_numeric(data_csv_2['Temperature'], errors='coerce')
#data_csv_2['Resistance'] = pd.to_numeric(data_csv_2['Resistance'], errors='coerce')

# Drop any rows with NaN values that could result from conversion errors
data_csv.dropna(inplace=True)
#data_csv_2.dropna(inplace=True)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data_csv['Temperature'], data_csv['Resistance'], color='blue', alpha=0.5, label = "First trial")
#plt.scatter(data_csv_2['Temperature'], data_csv_2['Resistance'], color='blue', alpha=0.5, label = "Second trial")
plt.title('Resistance vs. Temperature February 27th, 2024')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.grid(True)
plt.show()


#%% Average resistance from no temp change
average_resistance = data_csv['Resistance'].mean()

# Print the average resistance
print("Average Resistance:", average_resistance)

