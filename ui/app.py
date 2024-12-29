import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Rozpoznawanie Konstelacji", page_icon="✨", layout="centered")

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
    # Dodanie obrazu tła
    add_background_image("https://static.vecteezy.com/system/resources/thumbnails/019/856/500/small_2x/motion-of-shinny-stars-animation-on-black-background-night-stars-skies-with-twinkling-or-blinking-stars-motion-background-looping-seamless-space-backdrop-travel-free-video.jpg")

    # Nagłówek aplikacji
    st.title("🌌 Rozpoznawanie Konstelacji")
    st.write("""
    Prześlij zdjęcie nieba z widocznymi konstelacjami, aby dowiedzieć się, jaka to konstelacja. 
    Obecnie obsługujemy zdjęcia w formatach JPG i PNG.
    """)

    # Sekcja przesyłania obrazu
    uploaded_file = st.file_uploader("Wgraj zdjęcie", type=["jpg", "jpeg", "png"])
    
    # Placeholder na wyniki
    prediction_placeholder = st.empty()

    if uploaded_file is not None:
        # Wyświetlenie przesłanego obrazu
        st.image(uploaded_file, caption="Przesłane zdjęcie", use_column_width=True)

        # Przycisk do uruchomienia przewidywania (logika backendu do dodania później)
        if st.button("Rozpoznaj konstelację"):
            # TODO: Tutaj podłącz backend modelu do przewidywań
            prediction_placeholder.subheader("Przewidywanie: ⏳ Model w trakcie implementacji...")
        else:
            prediction_placeholder.subheader("Kliknij przycisk, aby uruchomić przewidywanie.")

    else:
        st.info("Proszę przesłać zdjęcie nieba.")

    # Sekcja stopki
    st.markdown("---")
    st.write("Aplikacja do rozpoznawania konstelacji ✨")

if __name__ == "__main__":
    main()
