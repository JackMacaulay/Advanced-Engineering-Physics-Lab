import pandas as pd
import matplotlib.pyplot as plt

# Define a style for the plot
plt.style.use('seaborn-whitegrid')
plt.rcParams.update({'font.size': 12, 'figure.dpi': 500})

# Function to process and plot data from a CSV file
def process_and_plot(csv_path, label, needs_split):
    try:
        # Initial read of the CSV file
        data_csv = pd.read_csv(csv_path, skiprows=1, header=None)
        
        if needs_split:
            # Attempt to split the first column into 'Temperature' and 'Resistance'
            split_data = data_csv[0].str.split(',', expand=True)
            if split_data.shape[1] == 2:
                data_csv[['Temperature', 'Resistance']] = split_data
            else:
                raise ValueError("Split operation did not result in two columns.")
        else:
            data_csv.columns = ['Temperature', 'Resistance']
        
        # Convert to numeric, coercing errors to NaN, and drop NaN values
        data_csv['Temperature'] = pd.to_numeric(data_csv['Temperature'], errors='coerce')
        data_csv['Resistance'] = pd.to_numeric(data_csv['Resistance'], errors='coerce')
        data_csv.dropna(inplace=True)
        
        # Plot the data
        plt.scatter(data_csv['Temperature'], data_csv['Resistance'], label=label, alpha=0.75)
    except Exception as e:
        print(f"Error processing file {csv_path}: {e}")


# List of CSV file paths, their labels, and whether they require splitting and cleaning
csv_files = [
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb13_Testing/Wafer_Test_Temp.csv", "Feb 13", True),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb15_Testing/Temp_Sweep.csv", "Feb 15 - 1", True),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb15_Testing/Temp_Sweep_2.csv", "Feb 15 - 2", True),
    ("C:/Users/jackm/OneDrive - Queen's University/Queen's Engineering/Fourth Year/ENPH 453/Advanced-Engineering-Physics-Lab/Semiconductor_Bandgap_Measurements/Feb27_Testing/Temp_Sweep.csv", "Feb 27", False)
]

# Marker styles for differentiation
markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', '+', 'x']

# Plot settings
plt.figure(figsize=(10, 6))

# Process each file
for path, label, needs_split in csv_files:
    process_and_plot(path, label, needs_split)

# Finalize plot
plt.title('Resistance vs. Temperature')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistance (Ohms)')
plt.legend()
plt.grid(True)
plt.show()
