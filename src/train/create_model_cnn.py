import os
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
from visualization import add_progress_visualization

if __name__=='__main__':
    data_dir = os.path.abspath("data/constellations")
    output_dir = os.path.abspath("models")

    # Parameters for image size and batch size
    batch_size = 16
    img_height = 224
    img_width = 224
    epochs = 32

    # Loading training and validation datasets with 8/2 ratio
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    # Get the class names from the dataset
    class_names = train_ds.class_names
    print("Class names:", class_names)

    # Improve performance by caching and prefetching the datasets
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Normalize pixel values to [0, 1]
    normalization_layer = layers.Rescaling(1. / 255)

    # Data augmentation layers
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomTranslation(0.1, 0.1),
        layers.RandomBrightness(0.1)
    ])

    # Apply data augmentation(only to the training dataset) and normalization to the datasets
    train_ds = train_ds.map(lambda x, y: (data_augmentation(normalization_layer(x)), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    num_classes = len(class_names)

    # Build the model
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    # Compile the model
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )

    # Callbacks
    early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=8,  # Stop training if validation loss doesn't improve for 5 epochs
    restore_best_weights=True  # Restore the model to the best weights
    )

    # Train the model
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[early_stopping]
    )

    # Visualize the training progress
    add_progress_visualization(history)

    # Save the trained model
    model.save(os.path.join(output_dir, "cnn_model.h5"))

    # TODO - Probably we should evaluate the model on the test set here
