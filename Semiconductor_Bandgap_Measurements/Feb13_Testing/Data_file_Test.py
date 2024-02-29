# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:42:03 2024

@author: jackm
This is for testing the formatting of the data files
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 
# Path to the CSV file
file_path = "C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb13_Testing/Temp_Sweep_13_Fixed.csv"
#data = pd.read_csv(file_path, skiprows=1, header=None, names=['Temperature', 'Resistance'])
data = pd.read_csv(file_path, skiprows=1)

print(data)