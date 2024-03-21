# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:40:44 2024

@author: jackm
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 300}) 

# Path to the CSV file
file_path = 'Semiconductor_Bandgap_Measurements\Mar05_Testing\Temp_Sweep_1_Sample_2.csv'
# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data = pd.read_csv(file_path, skiprows=1)


# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature'], data['Resistance'], color='blue', alpha=0.5)
plt.title('Sample 1: Resistance vs Temperature for Fixed T (Room Temp)')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.grid(True)
plt.show()

mean_resistance = data['Resistance'].mean()
median_resistance = data['Resistance'].median()
std_dev_resistance = data['Resistance'].std()
min_resistance = data['Resistance'].min()
max_resistance = data['Resistance'].max()

# Printing the statistics
print(f"Mean Resistance: {mean_resistance} Ohms")
print(f"Median Resistance: {median_resistance} Ohms")
print(f"Standard Deviation of Resistance: {std_dev_resistance} Ohms")
print(f"Minimum Resistance: {min_resistance} Ohms")
print(f"Maximum Resistance: {max_resistance} Ohms")

