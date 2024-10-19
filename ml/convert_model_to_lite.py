import os
import tensorflow as tf

from config import MODELS_DIR

# Load the best model
model = tf.keras.models.load_model(MODELS_DIR + "/best_model.keras")

# Convert the model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optional: Set the optimization strategy for the model
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Kwantyzacja

# Convert the model
tflite_model = converter.convert()

# Define the path to save the TFLite model
tflite_model_path = os.path.join(MODELS_DIR, "best_model.tflite")

# Save the TFLite model
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

print(f"Model saved to {tflite_model_path}")
