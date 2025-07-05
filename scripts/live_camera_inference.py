import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load your trained model
model = load_model("models/best_model.h5")
img_size = (224, 224)

# Open webcam (1 = external camera)
cap = cv2.VideoCapture(1)

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    h, w, _ = frame.shape
    # Calculate center rectangle coordinates
    rect_w, rect_h = img_size
    x1 = w // 2 - rect_w // 2
    y1 = h // 2 - rect_h // 2
    x2 = x1 + rect_w
    y2 = y1 + rect_h

    # Draw rectangle (focus area)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Crop the region inside the rectangle for inference
    roi = frame[y1:y2, x1:x2]
    if roi.shape[0] != rect_h or roi.shape[1] != rect_w:
        cv2.imshow("Live Camera Inference", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Show the ROI for debugging
    cv2.imshow("ROI", roi)

    # Preprocess ROI for model
    x = image.img_to_array(roi)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    # Inference
    pred = model.predict(x, verbose=0)[0][0]
    print("Raw model output:", pred)  # Debug: print raw output
    label = "Good" if pred > 0.5 else "Defective"
    confidence = pred if label == "Good" else 1 - pred

    # Display result on frame (above rectangle)
    text = f"{label} ({confidence*100:.2f}%)"
    color = (0, 255, 0) if label == "Good" else (0, 0, 255)
    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Live Camera Inference", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 