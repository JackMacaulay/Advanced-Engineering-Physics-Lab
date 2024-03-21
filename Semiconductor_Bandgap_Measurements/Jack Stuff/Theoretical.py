# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:39:09 2024

@author: jackm
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import Boltzmann
plt.style.use('seaborn-whitegrid')  # A clean and professional style
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500}) 

# Constants
Eg = 1.1  # Band gap energy of silicon in eV
kb = 8.617e-5  # Boltzmann's constant in eV/K
A = 1e-2  # Assumed constant for simplicity (not actual value)
mu_e = 1000  # Electron mobility in cm^2/(V·s), assumed constant
mu_h = 1000  # Hole mobility in cm^2/(V·s), assumed constant
T = np.linspace(200, 700, 1000)  # Temperature range from 200K to 500K

# Theoretical resistance calculation
R_T = (A / ((mu_e + mu_h) * T ** (3/2))) * np.exp(Eg / (2 * kb * T))

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(T, R_T, label='Theoretical Resistance', color = 'black', s = 5)
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.title('Theoretical Semiconductor Resistance vs. Temperature')
plt.yscale('log')  # Log scale for better visualization of exponential behavior
plt.legend()
plt.grid(True)
plt.show()
