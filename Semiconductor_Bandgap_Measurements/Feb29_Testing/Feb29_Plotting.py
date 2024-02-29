# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:16:01 2024

@author: jackm
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
# Path to the CSV file
file_path = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb29_Testing/Temp_Sweep.csv"

# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data = pd.read_csv(file_path, skiprows=1)



#%%
# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature'], data['Resistance'], color='blue', alpha=0.5)
plt.title('Resistance vs. Temperature')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.grid(True)
plt.show()
