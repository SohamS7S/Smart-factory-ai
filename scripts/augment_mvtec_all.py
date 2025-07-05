import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# === Path Config (your real MVTec location)
ROOT = r"D:\MVTecAD"
TARGET = r"D:\Smart_factory_ai\augmented"
AUGMENT_COUNT = 10

# === Image Augmentation Settings
datagen = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.5, 1.5],
    shear_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

def augment_folder(src_folder, dst_folder):
    os.makedirs(dst_folder, exist_ok=True)
    files = [f for f in os.listdir(src_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total = 0

    for file in files:
        img_path = os.path.join(src_folder, file)
        try:
            img = load_img(img_path)
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)
            base = os.path.splitext(file)[0]

            for i, batch in enumerate(datagen.flow(x, batch_size=1,
                                                   save_to_dir=dst_folder,
                                                   save_prefix=f"aug_{base}",
                                                   save_format='png')):
                if i >= AUGMENT_COUNT:
                    break
            total += AUGMENT_COUNT
        except Exception as e:
            print(f"⚠️ Failed on {file}: {e}")

    print(f"✅ {total} augmented images saved in: {dst_folder}")

# === Loop through all 15 categories
for category in os.listdir(ROOT):
    cat_path = os.path.join(ROOT, category)
    if not os.path.isdir(cat_path):
        continue

    # Train/good
    train_good = os.path.join(cat_path, 'train', 'good')
    if os.path.exists(train_good):
        print(f"🚀 Augmenting: {category}/train/good")
        augment_folder(train_good, os.path.join(TARGET, 'train', 'Good'))

    # Test/defective
    test_path = os.path.join(cat_path, 'test')
    if os.path.exists(test_path):
        for defect_type in os.listdir(test_path):
            defect_path = os.path.join(test_path, defect_type)
            if defect_type.lower() != "good" and os.path.isdir(defect_path):
                print(f"🚨 Augmenting: {category}/test/{defect_type}")
                augment_folder(defect_path, os.path.join(TARGET, 'train', 'Defective'))

print("\n🎉 DONE: All MVTec images augmented into D:\\Smart_factory_ai\\augmented")
