import os
import numpy as np
import pickle
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, Input
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger, Callback
from tensorflow.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_class_weight

# ========================
# 🔧 Configurations
# ========================
BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)
EPOCHS = 30
FINE_TUNE_AT = 10  # Unfreeze from this epoch
DATASET_DIR = "D:/Smart_factory_ai/dataset"  # or "/content/dataset" on Colab
MODEL_PATH = "best_model.h5"
HISTORY_PATH = "history.pkl"

# ========================
# 📁 Data Loaders
# ========================
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

# ========================
# ⚖️ Class Weights
# ========================
classes = train_gen.classes
class_weights = compute_class_weight('balanced', classes=np.unique(classes), y=classes)
class_weights = dict(enumerate(class_weights))
print("📊 Class Weights:", class_weights)

# ========================
# 🧠 Model Architecture
# ========================
base_model = MobileNetV2(weights='imagenet', include_top=False, input_tensor=Input(shape=(224, 224, 3)))
base_model.trainable = False  # Freeze initially

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=output)
model.compile(optimizer=Adam(learning_rate=1e-4), loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

# ========================
# 📦 Callbacks
# ========================
checkpoint = ModelCheckpoint(MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1)
earlystop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
csv_logger = CSVLogger('training_log.csv')

# 🛠️ Callback to unfreeze after N epochs
class UnfreezeCallback(Callback):
    def on_epoch_begin(self, epoch, logs=None):
        if epoch == FINE_TUNE_AT:
            print(f"\n🔓 Unfreezing base model at epoch {epoch}")
            base_model.trainable = True
            model.compile(optimizer=Adam(1e-5), loss='binary_crossentropy', metrics=['accuracy'])

# ========================
# 🚀 Training
# ========================
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen,
    class_weight=class_weights,
    callbacks=[checkpoint, earlystop, csv_logger, UnfreezeCallback()]
)

# ========================
# 💾 Save Training History
# ========================
with open(HISTORY_PATH, 'wb') as f:
    pickle.dump(history.history, f)

print("✅ Training complete. Best model saved as 'best_model.h5'")
