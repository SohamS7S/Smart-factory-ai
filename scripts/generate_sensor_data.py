import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# Parameters
n_normal = 1000
n_anomaly = 100
total = n_normal + n_anomaly

start_time = datetime(2025, 6, 1, 0, 0, 0)
timestamps = [start_time + timedelta(minutes=i) for i in range(total)]

# Normal data
vibration_normal = np.random.normal(loc=1.0, scale=0.05, size=n_normal)
temp_normal = np.random.normal(loc=37.0, scale=0.3, size=n_normal)
pressure_normal = np.random.normal(loc=2.4, scale=0.1, size=n_normal)

# Anomalous data
vibration_anom = np.random.normal(loc=3.0, scale=0.2, size=n_anomaly)
temp_anom = np.random.normal(loc=60.0, scale=2.5, size=n_anomaly)
pressure_anom = np.random.normal(loc=8.0, scale=0.5, size=n_anomaly)

# Combine
vibration = np.concatenate([vibration_normal, vibration_anom])
temp = np.concatenate([temp_normal, temp_anom])
pressure = np.concatenate([pressure_normal, pressure_anom])
labels = ['normal'] * n_normal + ['anomaly'] * n_anomaly

# Create DataFrame
df = pd.DataFrame({
    'timestamp': timestamps,
    'vibration': vibration,
    'temp': temp,
    'pressure': pressure,
    'label': labels
})

# Create output folder
os.makedirs('data/sensors', exist_ok=True)
df.to_csv('data/sensors/sensor_data.csv', index=False)
print("✅ sensor_data.csv generated successfully.")

# Optional: Plot to visualize
plt.figure(figsize=(10,4))
plt.plot(df['vibration'], label='Vibration')
plt.plot(df['temp'], label='Temperature')
plt.plot(df['pressure'], label='Pressure')
plt.axvline(x=n_normal, color='r', linestyle='--', label='Anomaly starts')
plt.legend()
plt.title("Simulated Sensor Data with Anomalies")
plt.tight_layout()
plt.savefig('data/sensors/sensor_plot.png')
plt.show()
