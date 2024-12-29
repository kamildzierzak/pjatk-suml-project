import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator

if __name__=='__main__':
    img_height = 224
    img_width = 224
    batch_size = 6
    num_classes = 88
    epochs = 30

    data_dir = "constellations"

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2  # Ustalanie 20% danych na walidację
    )

    # Normalizacja danych dla zbioru walidacyjnego i testowego
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    # Wczytanie danych treningowych
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),  # Rozmiar obrazów
        batch_size=8,
        class_mode='sparse',
        subset='training'  # Używamy 80% danych na trening
    )

    # Wczytanie danych walidacyjnych
    validation_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=8,
        class_mode='sparse',
        subset='validation'
    )

    # Używamy danych testowych (bez augmentacji, tylko normalizacja)
    test_generator = test_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),  # Rozmiar obrazów
        batch_size=8,
        class_mode='sparse'
    )

    base_model = MobileNetV2(input_shape=(img_height, img_width, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Zamrożenie warstw pretrenowanego modelu

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),  # Warstwa agregacji cech
        layers.Dense(128, activation='relu'),  # Warstwa w pełni połączona
        layers.Dropout(0.3),  # Regularizacja
        layers.Dense(num_classes, activation='softmax')  # Warstwa wyjściowa
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),  # Mała szybkość uczenia
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),  # Funkcja straty
        metrics=['accuracy']
    )

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,  # Zatrzymaj trening, jeśli walidacyjna strata nie poprawi się przez 5 epok
        restore_best_weights=True  # Przywróć najlepszą wagę modelu
    )

    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[early_stopping]
    )

    base_model.trainable = True  # Odblokowanie warstw pretrenowanego modelu
    fine_tune_at = 100  # Odmrożenie warstw od 100-tej warstwy

    # Zamrożenie warstw przed fine-tuningiem
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    # Ponowna kompilacja z mniejszym learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    # Fine-tuning modelu
    history_fine = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[early_stopping]
    )

    # Zapisanie modelu
    model.save('star_constellation_model.h5')
