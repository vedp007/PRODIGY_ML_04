# -*- coding: utf-8 -*-
"""Copy of convolutional_neural_network.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tPd5sG7I-yw8nEELDwwbrfA6uiIRoQDc

# Convolutional Neural Network

### Importing the libraries
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

data_dir = '/path/to/dataset'  # Replace with your LeapGestRecog dataset path
img_size = (64, 64)  # Resize images for faster training
batch_size = 32

"""## Part 1 - Data Preprocessing

### Preprocessing the Training set
"""

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2  # 80% train, 20% validation
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

"""### Preprocessing the Test set

## Part 2 - Building the CNN

### Initialising the CNN
"""

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation='softmax')
])

"""## Part 3 - Training the CNN

### Compiling the CNN
"""

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""### Training the CNN on the Training set and evaluating it on the Test set"""

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10
)

"""## Part 4 - Making a single prediction"""

test_loss, test_accuracy = model.evaluate(validation_generator)
print(f"Test Accuracy: {test_accuracy:.2f}")

model.save('gesture_recognition_model.h5')