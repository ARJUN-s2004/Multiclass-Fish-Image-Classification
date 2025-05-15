import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("fish_classifier_fast.h5")

model = load_model()

# Define class labels (replace with your actual classes)
class_names = ['animal fish', 'animal fish bass', 'fish sea_food black_sea_sprat', 'fish sea_food gilt_head_bream', 'fish sea_food hourse_mackerel', 
               'fish sea_food red_mullet', 'fish sea_food red_sea_bream', 'fish sea_food sea_bass', 'fish sea_food shrimp', 'fish sea_food striped_red_mullet', 'fish sea_food trout']

# Title
st.title("🐟 Fish Species Classifier")
st.write("Upload an image of a fish to identify its species.")

# Upload image
uploaded_file = st.file_uploader("Choose a fish image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess
    image = image.resize((160, 160))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)[0]
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions)

    # Display results
    st.markdown(f"### 🐠 Prediction: `{predicted_class}`")
    st.markdown(f"**Confidence:** `{confidence * 100:.2f}%`")

    # Confidence scores bar
    st.subheader("🔍 Confidence Scores")
    for i, prob in enumerate(predictions):
        st.write(f"{class_names[i]}: {prob*100:.2f}%")
        st.progress(int(prob * 100))
