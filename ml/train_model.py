import os
import tensorflow as tf

from tensorflow.keras import models, layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config import (
    DATA_DIR,
    MODELS_DIR,
    IMG_SIZE,
    BATCH_SIZE,
    EPOCHS,
    EPOCHS_FINE_TUNE,
    BACKBONES,
    DEFAULT_BACKBONE,
)
from utils.visualization import plot_training_history


def load_backbone(backbone_name):
    """
    Dynamically load the specified backbone model and preprocessing function.
    """
    if backbone_name not in BACKBONES:
        raise ValueError(
            f"Invalid backbone '{backbone_name}'. Choose from {list(BACKBONES.keys())}."
        )

    backbone = BACKBONES[backbone_name]
    model_class = backbone["model"]
    preprocess_func = backbone["preprocess"]

    model_module, model_name = model_class.rsplit(".", 1)
    preprocess_module, preprocess_name = preprocess_func.rsplit(".", 1)

    model_class = getattr(__import__(model_module, fromlist=[model_name]), model_name)
    preprocess_func = getattr(
        __import__(preprocess_module, fromlist=[preprocess_name]), preprocess_name
    )

    return (
        model_class(
            weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3)
        ),
        preprocess_func,
    )


def create_data_generators(preprocess_input):
    """
    Create data generators with augmentation.
    """
    datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.3,
        horizontal_flip=True,
        vertical_flip=True,
        rotation_range=180,
        zoom_range=0.3,
        channel_shift_range=25.0,
        brightness_range=[0.7, 1.3],
        shear_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
    )

    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training",
    )

    validation_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
    )

    return train_generator, validation_generator


def build_model(base_model, num_classes):
    """
    Build a transfer learning model on top of the base model.
    """
    # Freeze the convolutional layers of the pre-trained model
    base_model.trainable = False

    # Add new classification layers
    model = models.Sequential(
        [
            base_model,  # Add the pre-trained base model
            layers.GlobalAveragePooling2D(),  # Global Average Pooling layer to reduce dimensions
            layers.Dropout(0.35),
            layers.BatchNormalization(),  # Batch normalization layer
            layers.Dense(
                128,
                activation="relu",
                kernel_regularizer=tf.keras.regularizers.l2(0.02),
            ),
            layers.Dropout(0.5),
            layers.Dense(
                64,
                activation="relu",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            ),
            layers.Dense(
                num_classes, activation="softmax"
            ),  # Output layer (softmax for multi-class)
        ]
    )

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def train_model(backbone_name=DEFAULT_BACKBONE):
    """
    Train a model with the specified backbone.
    """
    base_model, preprocess_input = load_backbone(backbone_name)
    train_generator, validation_generator = create_data_generators(preprocess_input)

    print(train_generator.class_indices, len(train_generator.class_indices))

    model = build_model(base_model, len(train_generator.class_indices))

    # Define callbacks
    ## Early stopping to avoid overfitting
    early_stopping = EarlyStopping(
        monitor="val_loss", patience=3, restore_best_weights=True
    )
    checkpoint = ModelCheckpoint(
        os.path.join(MODELS_DIR, f"best_{backbone_name}_model.keras"),
        monitor="val_accuracy",
        save_best_only=True,
    )

    ## Reduce learning rate if the validation loss plateaus
    lr_scheduler = ReduceLROnPlateau(
        monitor="val_loss", factor=0.75, patience=10, min_lr=1e-6
    )

    # Train the model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        verbose=2,
        callbacks=[early_stopping, lr_scheduler],
    )

    plot_training_history(history)

    # Fine-tune: Unfreeze some layers of the pre-trained model
    for layer in base_model.layers[-10:]:
        layer.trainable = True

    # Recompile the model after unfreezing
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Fine-tune the model
    history_fine_tune = model.fit(
        train_generator,
        epochs=EPOCHS_FINE_TUNE,
        validation_data=validation_generator,
        verbose=2,
        callbacks=[early_stopping, checkpoint, lr_scheduler],
    )

    # Plot the fine-tuning progress
    plot_training_history(history_fine_tune)

    # Save the fine-tuned model
    model.save(os.path.join(MODELS_DIR, f"{backbone_name}_fine_tuned_model.keras"))
    print(f"Model saved to {MODELS_DIR}/{backbone_name}_fine_tuned_model.keras")


if __name__ == "__main__":
    train_model("efficientnet")
