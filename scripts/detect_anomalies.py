import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# === Load data ===
df = pd.read_csv("data/sensors/sensor_data.csv", parse_dates=["timestamp"])
features = ["vibration", "temp", "pressure"]

# === Load scaler and scale full data ===
scaler_max = np.load("models/lstm_scaler.npy")
scaler = MinMaxScaler()
scaler.fit(np.zeros((1, len(features))))
scaler.scale_ = 1.0 / scaler_max
scaler.min_ = 0
scaler.data_max_ = scaler_max
df[features] = scaler.transform(df[features])

# === Create sliding sequences ===
def create_sequences(data, window_size=30):
    sequences = []
    for i in range(len(data) - window_size):
        seq = data[i:i+window_size]
        sequences.append(seq)
    return np.array(sequences)

window_size = 30
X = create_sequences(df[features].values, window_size)
timestamps = df["timestamp"].values[window_size:]
true_labels = df["label"].values[window_size:]

# === Load model ===
model = load_model("models/lstm_autoencoder.h5")

# === Predict and compute reconstruction error ===
X_pred = model.predict(X)
mse = np.mean(np.mean(np.square(X - X_pred), axis=2), axis=1)

# === Set dynamic threshold ===
threshold = np.percentile(mse, 95)  # top 5% of errors are considered anomalies
pred_labels = ["anomaly" if e > threshold else "normal" for e in mse]

# === Save results ===
results_df = pd.DataFrame({
    "timestamp": timestamps,
    "reconstruction_error": mse,
    "true_label": true_labels,
    "predicted_label": pred_labels
})
results_df.to_csv("data/sensors/anomaly_results.csv", index=False)

# === Plot ===
plt.figure(figsize=(12, 5))
plt.plot(results_df["timestamp"], mse, label="Reconstruction Error", alpha=0.8)
plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold = {threshold:.4f}")
plt.xticks(rotation=45)
plt.title("Sensor Anomaly Detection using LSTM Autoencoder")
plt.ylabel("Reconstruction Error")
plt.xlabel("Timestamp")
plt.legend()
plt.tight_layout()
plt.savefig("history/anomaly_detection.png")
plt.show()

print("✅ Anomaly detection complete.")
