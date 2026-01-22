import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tkinter as tk
from tkinter import filedialog
import os

# incarca modelul
data_dir = r"C:\Users\Cristian Robert\Desktop\proiect-rn-Cristian-Robert\data\dummy"
model = load_model('./bird_classifier_mobilenet.h5')

# definesc etichetele speciilor
class_labels = sorted([f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))])
print(f"Specii detectate în folder: {class_labels}")

def predict_bird():
    # fereastra de selectie 
    root = tk.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename()
    
    if not img_path:
        print("Nicio imagine selectată.")
        return

    # verificarea extensiei fisierului
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    if not img_path.lower().endswith(valid_extensions):
        print(f"Eroare: Fișierul {img_path} nu este o imagine validă!")
        return

    try:
        print(f"Se procesează imaginea: {img_path}")
        # preproc
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # pred
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions[0])
        confidence = predictions[0][predicted_index] * 100

        print("-" * 30)
        print(f"Rezultat: {class_labels[predicted_index]}")
        print(f"Încredere: {confidence:.2f}%")
        print("-" * 30)
        
    except Exception as e:
        print(f"A apărut o eroare la citirea imaginii: {e}")

predict_bird()