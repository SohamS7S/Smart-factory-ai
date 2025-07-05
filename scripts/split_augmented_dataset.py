import os
import shutil
import random

# Config
input_base = r"D:\Smart_factory_ai\augmented\train"
output_base = r"D:\Smart_factory_ai\dataset"
classes = ["Good", "Defective"]
split_ratio = 0.8  # 80% training, 20% validation

# Cleanup
for split in ["train", "val"]:
    for cls in classes:
        target_path = os.path.join(output_base, split, cls)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        os.makedirs(target_path)

# Splitting function
def split_and_copy(class_name):
    src = os.path.join(input_base, class_name)
    all_files = [f for f in os.listdir(src) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    random.shuffle(all_files)

    split_idx = int(len(all_files) * split_ratio)
    train_files = all_files[:split_idx]
    val_files = all_files[split_idx:]

    for f in train_files:
        shutil.copy(os.path.join(src, f), os.path.join(output_base, "train", class_name))
    for f in val_files:
        shutil.copy(os.path.join(src, f), os.path.join(output_base, "val", class_name))

    print(f"✅ {class_name}: {len(train_files)} train, {len(val_files)} val")

# Run split
print("📂 Splitting augmented dataset...")
for cls in classes:
    split_and_copy(cls)

print("\n🎉 Dataset is ready at:", output_base)
