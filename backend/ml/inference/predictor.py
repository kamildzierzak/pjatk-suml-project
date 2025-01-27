import tensorflow as tf
import numpy as np

from ml.ml_config import MLConfig
from ml.inference.preprocess import preprocess_image


class Predictor:
    def __init__(self, model_path):
        try:
            self.model = tf.keras.models.load_model(model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def predict(self, image):
        if not self.model:
            raise ValueError("Model is not loaded.")
        processed_image = preprocess_image(image)
        predictions = self.model.predict(processed_image)
        predicted_class = MLConfig.CLASS_NAMES[np.argmax(predictions)]
        confidence = float(np.max(predictions))
        return predicted_class, confidence
