# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:18:17 2024

@author: jackm
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
# Path to the CSV file
file_path = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Mar05_Testing/Temp_Sweep_3_Sample_2.csv"


# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data = pd.read_csv(file_path, skiprows=1)
#data_2 = pd.read_csv(file_path_2, skiprows = 1)



#%%
# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data['Temperature'], data['Resistance'], color='blue', alpha=0.5, label = 'Trial 1')
#plt.scatter(data_2['Temperature'], data_2['Resistance'], color = 'red', alpha = 0.5, label = 'Trial 2')
plt.title('Resistance vs. Temperature, 29/02/2024')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.ylim(-15000, 15000)
plt.legend()
plt.grid(True)
plt.show()
