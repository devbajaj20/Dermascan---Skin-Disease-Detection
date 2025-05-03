import os
import pandas as pd

def count_images_per_set(train_dir, test_dir):
    def count_images_in_directory(directory):
        total = 0
        for class_name in os.listdir(directory):
            class_path = os.path.join(directory, class_name)
            if os.path.isdir(class_path):
                total += len([file for file in os.listdir(class_path) if file.endswith(('.png', '.jpg', '.jpeg'))])
        return total

    train_count = count_images_in_directory(train_dir)
    test_count = count_images_in_directory(test_dir)

    data = {
        'Dataset': ['Training', 'Testing'],
        'Number of Images': [train_count, test_count]
    }

    df = pd.DataFrame(data)
    print(df.to_markdown(index=False))  # Pretty table in terminal
    return df

# Example usage
train_folder = r'C:\Users\Divya Bajaj\Desktop\STUDY\Projects\New folder (2)\MINI PROJECT\Skin-Disease-Detection-Final\dataset\train'
test_folder = r'C:\Users\Divya Bajaj\Desktop\STUDY\Projects\New folder (2)\MINI PROJECT\Skin-Disease-Detection-Final\dataset\test'
  # change to your actual test folder

count_images_per_set(train_folder, test_folder)
