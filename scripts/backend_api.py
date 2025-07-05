from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
from PIL import Image
import uvicorn
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Load dotenv
load_dotenv()

# Load models with error handling
try:
    IMG_MODEL_PATH = os.getenv("IMG_MODEL_PATH", "models/best_model.h5")
    SENSOR_MODEL_PATH = os.getenv("SENSOR_MODEL_PATH", "models/lstm_autoencoder.h5")
    SCALER_PATH = os.getenv("SCALER_PATH", "models/lstm_scaler.npy")

    img_model = load_model(IMG_MODEL_PATH)
    sensor_model = load_model(SENSOR_MODEL_PATH)
    scaler_max = np.load(SCALER_PATH)
except Exception as e:
    logger.error(f"Error loading models: {e}")
    raise RuntimeError(f"Model loading failed: {e}")

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(np.zeros((1, 3)))
scaler.scale_ = 1.0 / scaler_max
scaler.min_ = 0
scaler.data_max_ = scaler_max

app = FastAPI(title="Smart Factory AI Backend", description="API for image and sensor anomaly detection.")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    vibration: float
    temp: float
    pressure: float

@app.post("/predict-image/", summary="Predict image quality", description="Classifies an uploaded image as Good or Defective.")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img = img.resize((224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0
        pred = img_model.predict(x, verbose=0)[0][0]
        label = "Good" if pred > 0.5 else "Defective"
        confidence = float(pred if label == "Good" else 1 - pred)
        logger.info(f"Image prediction: label={label}, confidence={confidence}")
        return {"label": label, "confidence": confidence}
    except Exception as e:
        logger.error(f"Image prediction error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/predict-sensor/", summary="Detect sensor anomaly", description="Detects anomalies in sensor data using an LSTM autoencoder.")
async def predict_sensor(data: SensorData):
    try:
        features = np.array([[data.vibration, data.temp, data.pressure]])
        features_scaled = scaler.transform(features)
        window_size = int(os.getenv("WINDOW_SIZE", 30))
        seq = np.repeat(features_scaled[np.newaxis, :, :], window_size, axis=1)
        recon = sensor_model.predict(seq, verbose=0)
        error = float(np.mean((seq - recon) ** 2))
        threshold = float(os.getenv("ANOMALY_THRESHOLD", 0.001))
        is_anomaly = error > threshold
        logger.info(f"Sensor prediction: anomaly={is_anomaly}, error={error}")
        return {"anomaly": is_anomaly, "reconstruction_error": error}
    except Exception as e:
        logger.error(f"Sensor prediction error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 