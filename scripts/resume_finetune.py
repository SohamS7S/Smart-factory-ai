import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger

# === CONFIG ===
BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)
EPOCHS = 30
START_EPOCH = 10
DATASET_DIR = "D:/Smart_factory_ai/dataset"
MODEL_PATH = "best_model.h5"
HISTORY_PATH = "history_finetune.pkl"

# === Load Model and Unfreeze Base ===
model = load_model(MODEL_PATH)
model.trainable = True  # Unfreeze entire model

model.compile(optimizer=Adam(1e-5), loss='binary_crossentropy', metrics=['accuracy'])

# === Data Loaders ===
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    os.path.join(DATASET_DIR, "train"),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary"
)
val_gen = val_datagen.flow_from_directory(
    os.path.join(DATASET_DIR, "val"),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

# === Class Weights ===
from sklearn.utils.class_weight import compute_class_weight
classes = train_gen.classes
class_weights = compute_class_weight('balanced', classes=np.unique(classes), y=classes)
class_weights = dict(enumerate(class_weights))
print("Class weights:", class_weights)

# === Callbacks ===
checkpoint = ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1)
earlystop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
csv_logger = CSVLogger("resume_training_log.csv", append=True)

# === Resume Training from Epoch 11 onward ===
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    initial_epoch=START_EPOCH,
    validation_data=val_gen,
    class_weight=class_weights,
    callbacks=[checkpoint, earlystop, csv_logger]
)

# === Save Updated History ===
with open(HISTORY_PATH, 'wb') as f:
    pickle.dump(history.history, f)

print("✅ Fine-tuning resumed and completed. Model saved.")
