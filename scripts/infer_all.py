import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from utils.alert_engine import send_alert
import pandas as pd

model = load_model("models/best_model.h5")

img_dir = "test_images"
img_size = (224, 224)

print(f"\n🔍 Running inference on all images in: {img_dir}\n")

results = []

for fname in sorted(os.listdir(img_dir)):
    if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    path = os.path.join(img_dir, fname)
    img = image.load_img(path, target_size=img_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    pred = model.predict(x, verbose=0)[0][0]
    label = "Good" if pred > 0.5 else "Defective"
    confidence = pred if label == "Good" else 1 - pred

    print(f"🖼️ {fname:<20} → {label:<10} ({confidence*100:.2f}% confident)")

    # Collect results for CSV
    results.append({
        'filename': fname,
        'label': label,
        'confidence': confidence
    })

    if label == "Defective":
        send_alert(
            title="Visual Defect Detected ⚠️",
            message=f"{fname} classified as DEFECTIVE with {confidence*100:.2f}% confidence."
        )

print("\n✅ All images processed.")

# Save results to CSV
os.makedirs('logs', exist_ok=True)
pd.DataFrame(results).to_csv('logs/image_inference_results.csv', index=False)
print("\n📝 Results saved to logs/image_inference_results.csv")
