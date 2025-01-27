import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50, MobileNetV2, EfficientNetB0
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.mobilenet_v2 import (
    preprocess_input as mobilenet_preprocess,
)
from tensorflow.keras.applications.efficientnet import (
    preprocess_input as efficientnet_preprocess,
)
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from ml.utils.visualization import plot_training_history

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "../../models")

# Set constants
IMG_SIZE = 224
BATCH_SIZE = 12
EPOCHS = 16
EPOCHS_FINE_TUNE = 8

# Choose your backbone: 'resnet', 'mobilenet', or 'efficientnet'
# BACKBONE = 'resnet'
# BACKBONE = 'mobilenet'
BACKBONE = "efficientnet"

if BACKBONE == "resnet":
    base_model = ResNet50(
        weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    preprocess_input = resnet_preprocess
elif BACKBONE == "mobilenet":
    base_model = MobileNetV2(
        weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    preprocess_input = mobilenet_preprocess
elif BACKBONE == "efficientnet":
    base_model = EfficientNetB0(
        weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    preprocess_input = efficientnet_preprocess
else:
    raise ValueError(
        "Invalid BACKBONE. Choose from 'resnet', 'mobilenet', or 'efficientnet'."
    )

# Data Preprocessing and Augmentation
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,  # Preprocess input based on the chosen backbone
    validation_split=0.2,  # Split data into training and validation
    horizontal_flip=True,  # Augmentation: horizontal flip
    rotation_range=5,  # Augmentation: random rotation
    zoom_range=0.2,  # Augmentation: random zoom
    brightness_range=[0.9, 1.1],  # Augmentation: random brightness adjustment
    # channel_shift_range=25.0  # Augmentation: random channel shift
)

# Flow images from the directory and apply preprocessing
train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),  # Resize images
    batch_size=BATCH_SIZE,
    class_mode="categorical",  # Multi-class classification
    subset="training",  # Use this subset for training
)

validation_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",  # Use this subset for validation
)

# Load the pre-trained ResNet50 model, without the top layer
base_model = ResNet50(
    weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Freeze the convolutional layers of the pre-trained model
base_model.trainable = False

# Create the new model
model = models.Sequential(
    [
        base_model,  # Add the pre-trained base model
        layers.GlobalAveragePooling2D(),  # Global Average Pooling layer to reduce dimensions
        layers.BatchNormalization(),  # Batch normalization layer
        layers.Dense(
            256, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)
        ),
        layers.Dropout(0.80),
        layers.Dense(
            128, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)
        ),
        layers.Dense(
            len(train_generator.class_indices), activation="softmax"
        ),  # Output layer (softmax for multi-class)
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Define callbacks
## Early stopping to avoid overfitting
early_stopping = EarlyStopping(
    monitor="val_loss", patience=3, restore_best_weights=True
)

## Save the best model based on validation accuracy
checkpoint = ModelCheckpoint(
    os.path.join(MODELS_DIR, f"best_{BACKBONE}_based_model.keras"),
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
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
    callbacks=[early_stopping, checkpoint, lr_scheduler],
)

plot_training_history(history)

# Fine-tune: Unfreeze some layers of the pre-trained model
for layer in base_model.layers[-30:]:
    layer.trainable = True

# Recompile the model after unfreezing
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# Define callbacks for fine-tuning
## Save the best model based on validation accuracy during fine-tuning
checkpoint_fine_tuned_model = ModelCheckpoint(
    os.path.join(MODELS_DIR, f"best_fined_tuned_{BACKBONE}_based_model.keras"),
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
)

# Fine-tune the model
history_fine_tune = model.fit(
    train_generator,
    epochs=EPOCHS_FINE_TUNE,  # Optionally, change the number of epochs for fine-tuning
    validation_data=validation_generator,
    verbose=2,
    callbacks=[early_stopping, checkpoint, lr_scheduler, checkpoint_fine_tuned_model],
)

# Plot the fine-tuning progress
plot_training_history(history_fine_tune)

# Save the fine-tuned model
model.save(
    os.path.join(
        MODELS_DIR, f"constellation_recognition_fine_tuned_{BACKBONE}_model.keras"
    )
)

# Evaluate the model on the validation set
test_loss, test_acc = model.evaluate(validation_generator)
print(f"Test accuracy: {test_acc}")
