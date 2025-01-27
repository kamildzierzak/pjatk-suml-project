import os
import logging
import tensorflow as tf
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from PIL import Image

from config import Config
from services.storage import upload_file_to_storage
from services.database import insert_prediction, fetch_history, delete_prediction
from utils.validation import allowed_file
from ml.ml_config import MLConfig
from ml.inference.predictor import Predictor

import random

# Disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Setup Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": Config.ALLOWED_ORIGINS}})

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase client
sb = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

# Initialize the model
predictor = Predictor(MLConfig.MODEL_PATH)


@app.route("/")
def home():
    """
    A basic route to confirm the application is running.
    """
    return "Hello, friend! Welcome to the Constellation Recognizer 6001X Deluxe API!"


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Handle file uploads, perform prediction, and store results.

    Request:
    - Form-data with:
      - 'image': File to upload (required)
      - 'user_id': User identifier (required)
      - 'model_id': Model identifier (optional, defaults to 'cnn')

    Steps:
    1. Validate and process the uploaded file.
    2. Upload the file to Supabase Storage.
    3. Perform a prediction using the model.
    4. Save prediction details to the database.
    5. Return the prediction result.
    """
    file = request.files.get("image")
    user_id = request.form.get("user_id")
    model_id = request.form.get("model_id", "cnn")

    # Validate input
    if not file or not user_id:
        logger.error("Missing file or user_id in the request.")
        return jsonify({"error": "Missing file or user_id"}), 400

    # Validate file type
    if not allowed_file(file.filename):
        logger.error("Invalid file type provided.")
        return (
            jsonify({"error": "Invalid file type. Only JPG, JPEG, PNG allowed."}),
            400,
        )

    # Upload file to storage
    public_url, error = upload_file_to_storage(sb, Config.BUCKET_NAME, file, user_id)
    if error:
        logger.error(f"File upload to storage failed: {error}")
        return jsonify({"error": error}), 500

    # Make prediction
    try:
        predicted_class, confidence = predictor.predict(file)
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        return jsonify({"error": "Error making prediction"}), 500

    # Save prediction to database
    success, error = insert_prediction(
        sb, Config.TABLE_NAME, user_id, file.filename, public_url, predicted_class
    )
    if not success:
        logger.error(f"Failed to save prediction to database: {error}")
        return jsonify({"error": error}), 500

    return jsonify(
        {"label": predicted_class, "confidence": confidence, "file_url": public_url}
    )


@app.route("/api/history", methods=["GET"])
def get_history():
    """
    Retrieve a user's prediction history.

    Query Parameters:
    - user_id (required): Fetch history for this user.

    Response:
    - List of prediction records, including file URLs and labels.
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    history, error = fetch_history(sb, Config.TABLE_NAME, user_id)
    if error:
        return jsonify({"error": error}), 500

    return jsonify(history), 200


@app.route("/api/history/<int:pred_id>", methods=["DELETE"])
def delete_history_item(pred_id):
    """
    Delete a prediction record and associated file.

    Steps:
    1. Fetch the prediction record from the database.
    2. Parse the file path from the record.
    3. Remove the file from Supabase Storage.
    4. Delete the record from the database.
    """
    response, error = delete_prediction(
        sb, Config.TABLE_NAME, Config.BUCKET_NAME, pred_id
    )

    if error:
        if error == "Prediction not found":
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 500

    return jsonify(response), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
