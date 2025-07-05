import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, RepeatVector, TimeDistributed, Dense
from tensorflow.keras.callbacks import EarlyStopping

# === Load Data ===
df = pd.read_csv("data/sensors/sensor_data.csv", parse_dates=["timestamp"])
df_normal = df[df["label"] == "normal"].copy()

features = ["vibration", "temp", "pressure"]
scaler = MinMaxScaler()
df_normal[features] = scaler.fit_transform(df_normal[features])

# === Create Sliding Windows ===
def create_sequences(data, window_size=30):
    sequences = []
    for i in range(len(data) - window_size):
        seq = data[i:i+window_size]
        sequences.append(seq)
    return np.array(sequences)

window_size = 30
X_train = create_sequences(df_normal[features].values, window_size)
print(f"✅ Training sequences shape: {X_train.shape}")  # (samples, time_steps, features)

# === Build LSTM Autoencoder ===
model = Sequential([
    LSTM(64, activation="relu", input_shape=(window_size, len(features)), return_sequences=False),
    RepeatVector(window_size),
    LSTM(64, activation="relu", return_sequences=True),
    TimeDistributed(Dense(len(features)))
])
model.compile(optimizer="adam", loss="mse")
model.summary()

# === Train ===
early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
history = model.fit(X_train, X_train, epochs=50, batch_size=32, callbacks=[early_stop], verbose=1)

# === Save Model & Scaler ===
os.makedirs("models", exist_ok=True)
model.save("models/lstm_autoencoder.h5")
np.save("models/lstm_scaler.npy", scaler.data_max_)

# === Plot Training Loss ===
plt.plot(history.history["loss"])
plt.title("LSTM Autoencoder Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.tight_layout()
plt.savefig("history/lstm_training_loss.png")
plt.show()
