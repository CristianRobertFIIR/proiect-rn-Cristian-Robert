import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing import image

# configurarea cailor locale
data_dir = r"C:\Users\Cristian Robert\Desktop\proiect-rn-Cristian-Robert\data\train" 
model_save_path = r'C:\Users\Cristian Robert\Desktop\proiect-rn-Cristian-Robert\models'

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 64
VALIDATION_SPLIT = 0.2
EPOCHS = 11



print("Disponibilitate GPU:", tf.config.list_physical_devices('GPU'))

# generare date
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=VALIDATION_SPLIT,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

NUM_CLASSES = train_generator.num_classes
class_labels = list(train_generator.class_indices.keys())

#construire model
base_model = MobileNetV2(input_shape=IMAGE_SIZE + (3,), include_top=False, weights='imagenet')
base_model.trainable = False

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1024, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#inceperea antrenamentului
print("Incepe antrenarea modelului...")
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

#salvare model
model.save(model_save_path)

#functia de predictie
def predict_bird(img_path):
    img = image.load_img(img_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    print(f"\nPredictie: **{class_labels[predicted_index]}**")
    print(f"Incredere: {predictions[0][predicted_index] * 100:.2f}%")


import tkinter as tk
from tkinter import filedialog

def select_and_predict():
    root = tk.Tk()
    root.withdraw()
    
    #deschiderea ferestrei de dialog pentru selectarea imaginii
    file_path = filedialog.askopenfilename(
        title="Selectează o imagine cu o pasăre",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    
    if file_path:
        print(f"Fișier selectat: {file_path}")
        predict_bird(file_path)
    else:
        print("Nicio imagine selectată.")


select_and_predict()