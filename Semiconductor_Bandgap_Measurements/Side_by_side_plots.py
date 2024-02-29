import pandas as pd
import matplotlib.pyplot as plt

# Define a style for the plot
plt.style.use('seaborn-whitegrid')
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500})
std_dev = 3098.1443788354463
# Function to process and plot data from a CSV file
def process_and_plot(csv_path, label):
    try:
        # Initial read of the CSV file
        data_csv = pd.read_csv(csv_path, skiprows=1)        
        mean_resistance = data_csv['Resistance'].mean()
        # Plot the data
        plt.scatter(data_csv['Temperature'], data_csv['Resistance'], label=label, alpha=0.75)
        
        lower_bound = mean_resistance - std_dev
        upper_bound = mean_resistance + std_dev

        # Find min and max temperature for the width of the square
        min_temp = data_csv['Temperature'].min()
        max_temp = data_csv['Temperature'].max()

        # Plot a rectangle for one standard deviation of the resistance
        plt.gca().add_patch(plt.Rectangle((min_temp, lower_bound), max_temp - min_temp, 2*std_dev, color='green', alpha=0.1))

    except Exception as e:
        print(f"Error processing file {csv_path}: {e}")


# List of CSV file paths, their labels, and whether they require splitting and cleaning
csv_files = [
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb13_Testing/Temp_Sweep.csv", "Feb 13"),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb15_Testing/Temp_Sweep.csv", "Feb 15 - 1"),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb15_Testing/Temp_Sweep_2.csv", "Feb 15 - 2"),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb27_Testing/Temp_Sweep.csv", "Feb 27 - 1"),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb27_Testing/Temp_Sweep_2.csv", "Feb 27 - 2"),    
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb29_Testing/Temp_Sweep_2.csv", "Feb 29 - 1"),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb29_Testing/Temp_Sweep_2.csv", "Feb 29 - 2")
]

# Marker styles for differentiation
markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', '+', 'x']

# Plot settings
plt.figure(figsize=(10, 6))

# Process each file
for path, label in csv_files:
    process_and_plot(path, label)

# Finalize plot
plt.title('Resistance vs. Temperature all Trials Sample 1')
plt.ylim(-2000, 2000)
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.legend()
plt.grid(True)
plt.show()
