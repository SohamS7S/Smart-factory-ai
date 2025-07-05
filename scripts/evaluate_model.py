import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# === Load the trained model ===
model = load_model("model/best_model.h5")

# === Load the validation set ===
val_datagen = ImageDataGenerator(rescale=1./255)
val_gen = val_datagen.flow_from_directory(
    "dataset/val",
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=False  # Important to match predictions with labels
)

# === Confirm label mappings ===
print("✅ Class indices from val_gen:", val_gen.class_indices)
# Output should be: {'Defective': 0, 'Good': 1}

# === Make predictions ===
y_true = val_gen.classes
y_pred_probs = model.predict(val_gen)
y_pred = (y_pred_probs > 0.5).astype(int).flatten()

# === Classification report with corrected label order ===
print("\n📄 Classification Report (Corrected Labels):\n")
print(classification_report(y_true, y_pred, target_names=["Defective", "Good"]))

# === Confusion Matrix ===
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=["Defective", "Good"], yticklabels=["Defective", "Good"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

# === Training History Plot ===
with open("history/history_finetune.pkl", "rb") as f:
    history = pickle.load(f)

plt.figure(figsize=(12, 5))

# Accuracy
plt.subplot(1, 2, 1)
plt.plot(history["accuracy"], label="Train Accuracy")
plt.plot(history["val_accuracy"], label="Val Accuracy")
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

# Loss
plt.subplot(1, 2, 2)
plt.plot(history["loss"], label="Train Loss")
plt.plot(history["val_loss"], label="Val Loss")
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.show()
