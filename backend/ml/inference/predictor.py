import tensorflow as tf
import numpy as np

from ml.ml_config import MLConfig
from ml.inference.preprocess import preprocess_image


class Predictor:
    def __init__(self, model_path):
        try:
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def predict(self, image):
        if not self.interpreter:
            raise ValueError("Model is not loaded.")

        processed_image = preprocess_image(image)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(input_details[0]["index"], processed_image)
        self.interpreter.invoke()

        predictions = self.interpreter.get_tensor(output_details[0]["index"])

        predicted_class = MLConfig.CLASS_NAMES[np.argmax(predictions)]
        confidence = float(np.max(predictions))

        return predicted_class, confidence


# class Predictor:
#     def __init__(self, model_path):
#         try:
#             self.model = tf.keras.models.load_model(model_path)
#             print("Model loaded successfully.")
#         except Exception as e:
#             print(f"Error loading model: {e}")
#             self.model = None

#     def predict(self, image):
#         if not self.model:
#             raise ValueError("Model is not loaded.")
#         processed_image = preprocess_image(image)
#         predictions = self.model.predict(processed_image)
#         predicted_class = MLConfig.CLASS_NAMES[np.argmax(predictions)]
#         confidence = float(np.max(predictions))
#         return predicted_class, confidence
