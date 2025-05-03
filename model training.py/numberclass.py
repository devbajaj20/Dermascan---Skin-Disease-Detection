import os
from prettytable import PrettyTable  # pip install prettytable if not already installed

def count_images_per_class(data_dir):
    class_counts = {}
    if not os.path.exists(data_dir):
        return class_counts
    for class_name in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path):
            image_count = len([
                f for f in os.listdir(class_path)
                if os.path.isfile(os.path.join(class_path, f))
            ])
            class_counts[class_name] = image_count
    return class_counts

# ✅ Update these paths as needed
base_path = r'C:\Users\Divya Bajaj\Desktop\STUDY\Minor Project\Skin-Disease-Detection-Final\dataset'
train_dir = os.path.join(base_path, 'train')
val_dir   = os.path.join(base_path, 'val')
test_dir  = os.path.join(base_path, 'test')

# 📊 Get class-wise image counts
train_counts = count_images_per_class(train_dir)
val_counts   = count_images_per_class(val_dir)
test_counts  = count_images_per_class(test_dir)

# 📋 Create table
table = PrettyTable()
table.field_names = ["Class", "Train Images", "Validation Images", "Test Images"]

# 🧠 Collect all unique class names
all_classes = sorted(set(train_counts) | set(val_counts) | set(test_counts))

for cls in all_classes:
    train_count = train_counts.get(cls, 0)
    val_count   = val_counts.get(cls, 0)
    test_count  = test_counts.get(cls, 0)
    table.add_row([cls, train_count, val_count, test_count])

# 📢 Show the result
print(table)
