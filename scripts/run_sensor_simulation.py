import pandas as pd
import numpy as np
import time
import os
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from datetime import datetime

# === Paths ===
SOURCE_FILE = "data/sensors/sensor_data.csv"
LIVE_FEED_FILE = "data/sensors/live_sensor_feed.csv"
MODEL_PATH = "models/lstm_autoencoder.h5"
SCALER_PATH = "models/lstm_scaler.npy"

# === Load model and scaler ===
model = load_model(MODEL_PATH)
scaler_max = np.load(SCALER_PATH)
scaler = MinMaxScaler()
scaler.fit(np.zeros((1, 3)))
scaler.scale_ = 1.0 / scaler_max
scaler.min_ = 0
scaler.data_max_ = scaler_max

# === Global Plotting Vars ===
recon_errors = []
timestamps = []
threshold = None
window_size = 30

# === Thread: Stream Data ===
def stream_sensor_data():
    df = pd.read_csv(SOURCE_FILE)
    os.makedirs(os.path.dirname(LIVE_FEED_FILE), exist_ok=True)
    with open(LIVE_FEED_FILE, "w") as f:
        f.write("timestamp,vibration,temp,pressure,label\n")

    for i, row in df.iterrows():
        with open(LIVE_FEED_FILE, "a") as f:
            f.write(",".join(map(str, row.values)) + "\n")
        time.sleep(0.25)  # Simulate 4 Hz stream

# === Thread: Live Plot + Anomaly Detection ===
def update_plot(frame):
    global recon_errors, timestamps, threshold

    try:
        df_live = pd.read_csv(LIVE_FEED_FILE, parse_dates=["timestamp"])
        if len(df_live) < window_size:
            return

        # Take last window
        recent_data = df_live.iloc[-window_size:][["vibration", "temp", "pressure"]]
        recent_scaled = scaler.transform(recent_data)
        seq = recent_scaled[np.newaxis, :, :]

        # Predict
        recon = model.predict(seq, verbose=0)
        error = np.mean(np.square(recent_scaled - recon))
        timestamp = df_live.iloc[-1]["timestamp"]

        if threshold is None:
            # Estimate threshold dynamically after enough data
            history_data = df_live[["vibration", "temp", "pressure"]].values
            sequences = []
            for i in range(len(history_data) - window_size):
                sequences.append(scaler.transform(history_data[i:i+window_size]))
            sequences = np.array(sequences)
            preds = model.predict(sequences, verbose=0)
            mse = np.mean(np.mean(np.square(sequences - preds), axis=2), axis=1)
            threshold = np.percentile(mse, 95)
            print(f"📈 Dynamic Threshold: {threshold:.4f}")

        # Store
        recon_errors.append(error)
        timestamps.append(timestamp)

        # Plot
        ax.clear()
        ax.plot(timestamps, recon_errors, label="Reconstruction Error")
        ax.axhline(y=threshold, color="red", linestyle="--", label="Anomaly Threshold")
        ax.scatter(
            [timestamps[-1]],
            [recon_errors[-1]],
            color="red" if error > threshold else "green",
            s=100,
            label="Current"
        )
        ax.set_title("🔴 Live Anomaly Detection")
        ax.set_ylabel("Reconstruction Error")
        ax.set_xlabel("Time")
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
        plt.tight_layout()

        if error > threshold:
            print(f"🚨 [{timestamp}] Anomaly detected! Reconstruction error = {error:.4f}")

    except Exception as e:
        print("⚠️ Error:", e)

# === Run Threads ===
if __name__ == "__main__":
    # Start streaming in a thread
    t = threading.Thread(target=stream_sensor_data)
    t.start()

    # Plot setup
    fig, ax = plt.subplots(figsize=(12, 5))
    ani = FuncAnimation(fig, update_plot, interval=1000)
    plt.show()

    # Wait for streaming to finish
    t.join()
