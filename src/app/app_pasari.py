import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

#setari pagina 
st.set_page_config(page_title="Detector de Pasari")

st.title("Model de predictie pentru specii de Pasari")
st.write("Incarca o poza cu o pasare")

#incarc model
@st.cache_resource 
def load_bird_model():
    model = tf.keras.models.load_model('bird_classifier_mobilenet.h5')
    data_dir = r"C:\Users\Cristian Robert\Desktop\proiect-rn-Cristian-Robert\data\train"
    labels = sorted([f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))])
    return model, labels

try:
    model, class_labels = load_bird_model()
    st.success("Modelul a fost incarcat cu succes!")
except Exception as e:
    st.error(f"Eroare la incarcarea modelului: {e}")

# incarcarea imag
uploaded_file = st.file_uploader("Alege o imagine...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # afisare imagine
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagine incarcata', use_container_width=True)
    
    st.write("Se analizeaza...")
    
    # preproc
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # pred
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0]) 
    predicted_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_index] * 100

    # final
    st.subheader(f"Rezultat: **{class_labels[predicted_index]}**")
    st.progress(int(confidence))
    st.write(f"Nivel de încredere: {confidence:.2f}%")