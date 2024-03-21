# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:30:01 2024

@author: jackm
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
file_path = "Coil_calibration.csv"

# Read the CSV, skipping the initial incorrect header and split the 'Temperature,Resistance' combined column
data = pd.read_csv(file_path)
print(data)

#%%
# Fit a linear regression line
coefficients = np.polyfit(data['Current (mADC)'], 1000*data['Recorded Field'], 1)
linear_fit = np.poly1d(coefficients)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(data['Current (mADC)'], 1000*data['Recorded Field'], color='black', label='Data')
plt.plot(data['Current (mADC)'], linear_fit(data['Current (mADC)']), color='red', label='Linear Fit')
plt.title('Coil Magnetic Field over Current')
plt.xlabel('Current (mADC)')
plt.ylabel('Field (G)')
plt.grid(True)
plt.legend()
plt.show()

# Print the equation of the fit
print("Fit equation: {:.2f}x + {:.2f}".format(coefficients[0], coefficients[1]))
