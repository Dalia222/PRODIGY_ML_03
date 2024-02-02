# -*- coding: utf-8 -*-
"""Prodigy_Infotech_03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yJdZKRmWENaM5aetxq8xcRTGVfdDQ7xB
"""

import shutil
shutil.move("kaggle.json", "/root/.kaggle/kaggle.json")

!pip install --upgrade kaggle

!kaggle datasets download -d chetankv/dogs-cats-images

import os

dataset_path = '/content/Prodigy_03'
zip_file_path = os.path.join(dataset_path, 'dogs-cats-images.zip')  # Corrected file name

!mkdir -p ~/.kaggle
!cp "/content/drive/MyDrive/kaggle.json" ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Download the dataset
!kaggle datasets download -d chetankv/dogs-cats-images -p "{dataset_path}"  # Use correct dataset

# Check if the file exists
if os.path.exists(zip_file_path):
    # Unzip the dataset
    !unzip -q "{zip_file_path}" -d "{dataset_path}"
else:
    print("File does not exist.")

#@title Imports
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn import preprocessing
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from keras.preprocessing.image import ImageDataGenerator

#@title Datasets
dataset_path = '/content/Prodigy_03'
train_zip_path = os.path.join(dataset_path, 'train.zip')
test_zip_path = os.path.join(dataset_path, 'test1.zip')

# Unzip the training and testing datasets
!unzip -q "{train_zip_path}" -d "{dataset_path}"
!unzip -q "{test_zip_path}" -d "{dataset_path}"

#@title Load and preprocess images
def load_images(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        img = cv2.resize(img, (64, 64))  # Resize the image
        images.append(img.flatten())  # Flatten the image matrix
        labels.append(1 if "dog" in filename else 0)  # Assign label 1 for dogs, 0 for cats
    return np.array(images), np.array(labels)

# Load training set
train_cats, label_cats = load_images("/content/Prodigy_03/dog vs cat/dataset/training_set/cats")
train_dogs, label_dogs = load_images("/content/Prodigy_03/dog vs cat/dataset/training_set/dogs")

# Concatenate cat and dog data
X_train = np.concatenate((train_cats, train_dogs), axis=0)
y_train = np.concatenate((label_cats, label_dogs), axis=0)

#@title Feature scaling
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)

#@title Split the data into training and testing sets
X_train_final, X_test, y_train_final, y_test = train_test_split(X_train_scaled, y_train, test_size=0.2, random_state=42)

#@title Image augmentation
datagen = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
datagen.fit(X_train_final.reshape(-1, 64, 64, 1))

#@title Load and preprocess training images
# Create an SVM classifier with RBF kernel
batch_size = 32
clf = svm.SVC(kernel='rbf')

# Reshape the augmented data
augmented_data = datagen.flow(X_train_final.reshape(-1, 64, 64, 1), y_train_final, batch_size=batch_size)

# Extract augmented data
X_train_augmented, y_train_augmented = augmented_data[0][0].reshape(-1, 64 * 64), augmented_data[0][1]

# Fit the model with augmented data
clf.fit(X_train_augmented, y_train_augmented)

#@title Make predictions on the test set & Evaluate the model
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Print Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Print Classification Report
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)

# Extract precision, recall, and F1-score from the report
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print precision, recall, and F1-score
print(f"Precision: {precision:.4f}")
print(f"F1-Score: {f1:.4f}")