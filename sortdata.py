import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

# Load images and labels
def load_data(data_dir):
    images = []
    labels = []
    for label in os.listdir(data_dir):
        for img_file in os.listdir(os.path.join(data_dir, label)):
            img_path = os.path.join(data_dir, label, img_file)
            img = cv2.imread(img_path)
            if img is None:
                print("Error: Image not found or unable to load.")
            else:
                img = cv2.resize(img, (128, 128))  # Resize to desired dimensions
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

data_dir = "D:/Jiya/Apple___Apple_scab"
X, y = load_data(data_dir)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                  
