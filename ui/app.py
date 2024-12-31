import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("models/cnn_model.h5")
    # model = tf.keras.models.load_model("/models/mobilenetv2_model.h5")
    return model

def preprocess_image(raw_img):
    img = raw_img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# Styl CSS dla tła
def add_background_image(image_url: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_url});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Konfiguracja strony
    st.set_page_config(page_title="Rozpoznawanie Konstelacji", page_icon="✨", layout="centered")

    model = load_model()
    
    # Dodanie obrazu tła
    add_background_image("https://static.vecteezy.com/system/resources/thumbnails/019/856/500/small_2x/motion-of-shinny-stars-animation-on-black-background-night-stars-skies-with-twinkling-or-blinking-stars-motion-background-looping-seamless-space-backdrop-travel-free-video.jpg")

    # Nagłówek aplikacji
    st.title("🌌 Rozpoznawanie Konstelacji")
    st.write("""
    Prześlij zdjęcie nieba z widocznymi konstelacjami, aby dowiedzieć się, jaka to konstelacja. 
    Obecnie obsługujemy zdjęcia w formatach JPG, JPEG i PNG.
    """)

    # Sekcja przesyłania obrazu
    uploaded_file = st.file_uploader("Wgraj zdjęcie", type=["jpg", "jpeg", "png"])
    
    # Placeholder na wyniki
    prediction_placeholder = st.empty()

    if uploaded_file is not None:
        # Wyświetlenie przesłanego obrazu
        st.image(uploaded_file, caption="Przesłane zdjęcie", use_container_width=True)

        # Przetworzenie obrazu do formatu zgodnego z modelem
        img = image.load_img(uploaded_file)
        img_array = preprocess_image(img)

        # Przycisk do uruchomienia przewidywania (logika backendu do dodania później)
        if st.button("Rozpoznaj konstelację"):
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)

            class_names = ['Andromeda', 'Antlia', 'Apus', 'Aquarius', 'Aquila', 'Ara', 'Aries', 'Auriga', 'Bootes', 'Caelum', 'Camelopardalis', 'Cancer', 'Canes Venatici', 'Canis Maior', 'Canis Minor', 'Capricornus', 'Carina', 'Cassiopeia', 'Centaurus', 'Cepheus', 'Cetus', 'Chamaeleon', 'Circinus', 'Columba', 'Coma Berenices', 'Corona Australis', 'Corona Borealis', 'Corvus', 'Crater', 'Crux', 'Cygnus', 'Delphinus', 'Dorado', 'Draco', 'Equuleus', 'Eridanus', 'Fornax', 'Gemini', 'Grus', 'Hercules', 'Horologium', 'Hydra', 'Hydrus', 'Indus', 'Lacerta', 'Leo', 'Leo Minor', 'Lepus', 'Libra', 'Lupus', 'Lynx', 'Lyra', 'Mensa', 'Microscopium', 'Monoceros', 'Musca', 'Norma', 'Octans', 'Ophiuchus', 'Orion', 'Pavo', 'Pegasus', 'Perseus', 'Phoenix', 'Pictor', 'Pisces', 'Piscis Austrinus', 'Puppis', 'Pyxis', 'Reticulum', 'Sagitta', 'Sagittarius', 'Scorpius', 'Sculptor', 'Scutum', 'Serpens', 'Sextans', 'Taurus', 'Telescopium', 'Triangulum', 'Triangulum Australe', 'Tucana', 'Ursa Maior', 'Ursa Minor', 'Vela', 'Virgo', 'Volans', 'Vulpecula']
            predicted_label = class_names[predicted_class[0]]

            prediction_placeholder.subheader(f"Przewidywanie: {predicted_label}")
        else:
            prediction_placeholder.subheader("Kliknij przycisk, aby uruchomić przewidywanie.")

    else:
        st.info("Proszę przesłać zdjęcie nieba.")

    # Sekcja stopki
    st.markdown("---")
    st.write("Aplikacja do rozpoznawania konstelacji ✨")

if __name__ == "__main__":
    main()
