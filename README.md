# PJATK - Machine learning deployment and AutoML (SUML) - Project

## Deploy

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pjatk-suml-project-bo5gy2gqnlqkhtjqfavf9r.streamlit.app/)

## Dataset

[Dataset on GDrive](https://drive.google.com/drive/folders/17p_7q_MO6bWPaR_-Bg7lNkkfmHNYE4V7?usp=sharing)

By utworzyć więcej danych, można w programie [Stellarium 23.4](https://stellarium.org/) odpalić console (F12) i użyć skryptu 'create_dataset'.

## Model training

By zacząć z którymkolwiek skryptem do tworzenia modelu, wpierw należy pobrać dane `constellations` z gDrive i wrzucić do folderu `data`.

### CNN

Skrypt `create_model_cnn.py` do trenowania modelu CNN nie obsługuje polskich znaków, dlatego należy je usunąć z nazw plików w folderze `constellations`.

Można to zrobić skryptem `remove_polish_tranlations_from_constellations_folder.py`.

### MobileNetV2

Skrypt `create_model_mobilenetv2.py` do trenowania modelu MobileNetV2 nie wymaga usuwania polskich znaków z nazw plików w folderze `constellations`.

## Extra

- [Stellarium API](https://stellarium.org/doc/23.0/scripting.html)
- [Stellarium - Build-in Scripts](https://github.com/Stellarium/stellarium/tree/3db7943d1015aab2774f858b85b95a14c1e52f48/scripts)
