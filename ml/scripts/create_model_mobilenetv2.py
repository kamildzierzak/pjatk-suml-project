import os
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from ml.scripts.visualization import plot_training_history

if __name__ == "__main__":
    data_dir = os.path.abspath("data/constellations")
    output_dir = os.path.abspath("models")

    # Parametry dla rozmiaru obrazu i batch size
    img_height = 224
    img_width = 224
    batch_size = 16
    num_classes = 88
    epochs = 32

    # Augmentacja danych dla zbioru treningowego
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,  # Normalizacja pikseli do zakresu [0, 1]
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",  # Uzupełnianie pikseli po transformacji
        validation_split=0.2,  # Ustalanie 20% danych na walidację
    )

    # Normalizacja danych dla zbioru walidacyjnego i testowego
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)

    # Wczytanie danych treningowych
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(img_height, img_width),  # Rozmiar obrazów
        batch_size=batch_size,
        class_mode="sparse",
        subset="training",  # Używamy 80% danych na trening
    )

    # Wczytanie danych walidacyjnych
    validation_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode="sparse",
        subset="validation",
    )

    # Wczytanie danych testowych (bez augmentacji, tylko normalizacja)
    test_generator = test_datagen.flow_from_directory(
        data_dir,
        target_size=(img_height, img_width),  # Rozmiar obrazów
        batch_size=batch_size,
        class_mode="sparse",
    )

    # Wczytanie pretrenowanego modelu MobileNetV2
    base_model = MobileNetV2(
        input_shape=(img_height, img_width, 3), include_top=False, weights="imagenet"
    )
    base_model.trainable = False  # Zamrożenie warstw pretrenowanego modelu

    # Budowa modelu
    model = models.Sequential(
        [
            base_model,
            layers.GlobalAveragePooling2D(),  # Warstwa agregacji cech
            layers.Dense(128, activation="relu"),  # Warstwa w pełni połączona
            layers.Dropout(0.3),  # Regularizacja
            layers.Dense(num_classes, activation="softmax"),  # Warstwa wyjściowa
        ]
    )

    # Kompilacja modelu
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0001
        ),  # Mała szybkość uczenia
        loss=tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=False
        ),  # Funkcja straty
        metrics=["accuracy"],
    )

    # Callbacki
    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,  # Zatrzymaj trening, jeśli walidacyjna strata nie poprawi się przez 5 epok
        restore_best_weights=True,  # Przywróć najlepszą wagę modelu
    )

    # Uczenie modelu
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[early_stopping],
    )

    # Dostrojenie (fine-tuning) pretrenowanego modelu
    base_model.trainable = True  # Odblokowanie warstw pretrenowanego modelu
    fine_tune_at = 100  # Odmrożenie warstw od 100-tej warstwy

    # Zamrożenie warstw przed fine-tuningiem
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    # Ponowna kompilacja z mniejszym learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )

    # Dostojenie (fine-tuning) modelu z nowym learning rate
    history_fine = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[early_stopping],
    )

    # Wizualizacja postępu uczenia
    plot_training_history(history)

    # Zapisanie modelu
    model.save(os.path.join(output_dir, "mobilenetv2_model.h5"))

    # TODO - Prawdopodobnie powinniśmy jeszcze ewaluować model na danych testowych
