import os
import shutil

# 🗂️ Updated paths for D: drive
mvtec_root = r"D:\MVTecAD"
target_root = r"D:\Smart_factory_ai\dataset"

# Create unified Good/Defective folders
for split in ["train/Good", "val/Good", "val/Defective"]:
    os.makedirs(os.path.join(target_root, split), exist_ok=True)

# Loop through each object folder in MVTec
for obj in os.listdir(mvtec_root):
    obj_path = os.path.join(mvtec_root, obj)
    if not os.path.isdir(obj_path):
        continue

    print(f"📦 Processing: {obj}")

    # 1. Merge train/good → train/Good
    train_good = os.path.join(obj_path, "train", "good")
    if os.path.exists(train_good):
        for file in os.listdir(train_good):
            src = os.path.join(train_good, file)
            dst = os.path.join(target_root, "train", "Good", f"{obj}_{file}")
            shutil.copy(src, dst)

    # 2. Merge test/good → val/Good
    test_good = os.path.join(obj_path, "test", "good")
    if os.path.exists(test_good):
        for file in os.listdir(test_good):
            src = os.path.join(test_good, file)
            dst = os.path.join(target_root, "val", "Good", f"{obj}_{file}")
            shutil.copy(src, dst)

    # 3. Merge test/defect_type/* → val/Defective
    test_path = os.path.join(obj_path, "test")
    for defect_type in os.listdir(test_path):
        if defect_type == "good":
            continue
        defect_dir = os.path.join(test_path, defect_type)
        if os.path.isdir(defect_dir):
            for file in os.listdir(defect_dir):
                src = os.path.join(defect_dir, file)
                dst = os.path.join(target_root, "val", "Defective", f"{obj}_{defect_type}_{file}")
                shutil.copy(src, dst)

print("\n✅ Merged dataset is ready at:", target_root)
