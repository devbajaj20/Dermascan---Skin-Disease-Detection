import os
import shutil
import random

# Input and output directories
input_dir = "image"
output_base = "dataset"
splits = ["train", "val", "test"]
split_ratios = [0.8, 0.1, 0.1]

# Create output dirs
for split in splits:
    os.makedirs(os.path.join(output_base, split), exist_ok=True)

# Loop through disease folders
for folder in os.listdir(input_dir):
    if not os.path.isdir(os.path.join(input_dir, folder)):
        continue

    full_class_path = os.path.join(input_dir, folder)
    images = os.listdir(full_class_path)
    random.shuffle(images)

    # Extract clean class name (remove " Photos")
    class_name = folder.replace(" Photos", "")

    # Split into train/val/test
    n_total = len(images)
    n_train = int(split_ratios[0] * n_total)
    n_val = int(split_ratios[1] * n_total)

    split_data = {
        "train": images[:n_train],
        "val": images[n_train:n_train + n_val],
        "test": images[n_train + n_val:]
    }

    for split, split_imgs in split_data.items():
        split_class_dir = os.path.join(output_base, split, class_name)
        os.makedirs(split_class_dir, exist_ok=True)

        for img_name in split_imgs:
            src_path = os.path.join(full_class_path, img_name)
            dst_path = os.path.join(split_class_dir, img_name)
            shutil.copyfile(src_path, dst_path)

print("✅ Dataset split complete and saved under 'dataset/'")
