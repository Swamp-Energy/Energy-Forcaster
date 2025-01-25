import pandas as pd
import numpy as np

# Create a date range
date_range = pd.date_range(start="2023-01-01", end="2023-01-15", freq="H")  # Hourly data for 15 days

# Generate dummy data
np.random.seed(42)
data = {
    "datetime": date_range,
    "energy_consumption": np.random.randint(400, 600, size=len(date_range)),  # Energy usage in kWh
    "temperature": np.random.uniform(10, 35, size=len(date_range)),  # Temperature in °C
    "humidity": np.random.uniform(30, 90, size=len(date_range)),  # Humidity in %
    "population": np.random.randint(500000, 600000, size=len(date_range)),  # Population
}

# Create a DataFrame
dummy_data = pd.DataFrame(data)

# Save to a CSV file
file_path = "/mnt/data/energy_data.csv"
dummy_data.to_csv(file_path, index=False)

file_path
