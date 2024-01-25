"""
By: Jack Macaulay

Script that plots theoretical values of thermal noise
for ENPH453
"""
#%% Relevant libraries 

import matplotlib.pyplot as plt
import numpy as np

#%% Plots parameters
plt.rcParams['figure.dpi'] = 1000
#%% Parameters
time_constants = [1, 3, 10, 30, 100, 300]  # This is in seconds

# Conversion factors
micro_seconds_conversion = 10**-6
milli_seconds_conversion = 10**-3
kilo_seconds_conversion = 10**3

# Converting time constants
micro_seconds = [tc * micro_seconds_conversion for tc in time_constants]
milli_seconds = [tc * milli_seconds_conversion for tc in time_constants]
seconds = time_constants
kilo_seconds = [tc * kilo_seconds_conversion for tc in time_constants]

#print("Microseconds:", micro_seconds)
#print("Milliseconds:", milli_seconds)
#print("Seconds:", seconds)
#print("Kiloseconds:", kilo_seconds)

filter_values = [6, 12, 18, 24] #Units of dB/octave

resistance_values = [50, 0.998e6, 510e3, 250e3]

#Functions for plotting
def v_rms(R, enbw):
    k = 1.38e-23  # J/K, corrected Boltzmann's constant
    T = 300  # K - room temperature
    return np.sqrt(4 * k * T * R * enbw)


def combined_noise(v, f_list, alpha=0):
    johnson_noise = v  # Johnson noise is constant
    flicker_noise = [alpha / f for f in f_list]  # 1/f noise
    combined = [np.sqrt(jn**2 + fn**2) for jn, fn in zip(johnson_noise, flicker_noise)]
    return combined


#%% Theoretical plot for 50 Ohm 100 ms
#This is based on using the 18 dB/oct
enbw_test = 3/(32*milli_seconds[2])
r_test = resistance_values[1]

v_rms_test = v_rms(r_test, enbw_test)
frequencies_test = np.arange(10, 10000, 1)

noise_test = combined_noise([v_rms_test] * len(frequencies_test), frequencies_test)

print(noise_test)
plt.plot(frequencies_test, noise_test, color = 'black')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Frequencies [Hz]")
plt.ylabel("Noise [V/$\sqrt{Hz}$]")
plt.title(r"Theoretical Noise plots for $t = 10\ ms$ and $R = 0.998\ M\Omega$")
plt.grid()
plt.show()

