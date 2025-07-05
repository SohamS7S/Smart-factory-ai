import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import time
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.alert_engine import send_alert


# Paths
MODEL_PATH = "models/lstm_autoencoder.h5"
SCALER_PATH = "models/lstm_scaler.npy"
LIVE_FEED_PATH = "data/sensors/live_sensor_feed.csv"

# Load model & scaler
model = load_model(MODEL_PATH)
scaler_max = np.load(SCALER_PATH)

# Setup scaler
scaler = MinMaxScaler()
scaler.fit(np.zeros((1, 3)))
scaler.scale_ = 1.0 / scaler_max
scaler.min_ = 0
scaler.data_max_ = scaler_max

# Helper to make sliding windows
def create_sequence(data, window_size=30):
    if len(data) < window_size:
        return None
    return np.expand_dims(data[-window_size:], axis=0)

# Run
print("📡 Monitoring live sensor feed... (press Ctrl+C to stop)")
window_size = 30
prev_row_count = 0

try:
    while True:
        if os.path.exists(LIVE_FEED_PATH):
            df = pd.read_csv(LIVE_FEED_PATH)
            if len(df) != prev_row_count:
                prev_row_count = len(df)
                values = df[["vibration", "temp", "pressure"]].values
                values_scaled = scaler.transform(values)

                seq = create_sequence(values_scaled, window_size)
                if seq is not None:
                    recon = model.predict(seq, verbose=0)
                    error = np.mean((seq - recon) ** 2)

                    threshold = 0.001  # Set dynamically if needed
                    if error > threshold:
                        timestamp = df.iloc[-1]["timestamp"]
                        print(f"🚨 [{timestamp}] Anomaly detected! Reconstruction error = {error:.4f}")
                        send_alert("Sensor Anomaly Detected 🚨", f"At {timestamp} | Reconstruction Error: {error:.4f}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Monitoring stopped.")
