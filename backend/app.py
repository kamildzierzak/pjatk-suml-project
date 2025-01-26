import os
import random
import time
import logging

from flask import Flask, request, jsonify
from supabase import create_client, Client
from werkzeug.utils import secure_filename

# Testing
# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BUCKET_NAME = "images"
TABLE_NAME = "predictions"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_storage(file, user_id):
    """Upload a file to Supabase Storage and return its public URL."""
    try:
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_name = f"{user_id}_{int(time.time())}_{original_filename}"

        # Upload file to Supabase Storage
        file_bytes = file.read()
        upload_res = sb.storage.from_(BUCKET_NAME).upload(
            unique_name, file_bytes, {"contentType": file.mimetype}
        )
        if upload_res.get("error"):
            logger.error(f"File upload failed: {upload_res['error']}")
            return None, "File upload failed"

        # Get public URL
        public_url = sb.storage.from_(BUCKET_NAME).get_public_url(unique_name).get("publicURL")
        return public_url, None
    except Exception as e:
        logger.error(f"Exception during file upload: {e}")
        return None, "Internal server error during file upload"    

def insert_prediction(user_id, filename, file_url, label):
    """Insert a prediction record into the database."""
    try:
        prediction_data = {
            "user_id": user_id,
            "filename": filename,
            "file_url": file_url,
            "label": label,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        db_res = sb.table(TABLE_NAME).insert(prediction_data).execute()
        if db_res.error:
            logger.error(f"Failed to insert prediction: {db_res.error}")
            return False, "Failed to save prediction"
        return True, None
    except Exception as e:
        logger.error(f"Exception during prediction insertion: {e}")
        return False, "Internal server error during prediction insertion"

@app.route('/')
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
        return jsonify({"error": "Missing file or user_id"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, PNG allowed."}), 400

    # Upload file to storage
    public_url, error = upload_file_to_storage(file, user_id)
    if error:
        return jsonify({"error": error}), 500

    # Mock prediction (replace with actual ML model logic)
    possible_labels = ["Orion", "Cassiopeia", "Ursa Major"]
    label = random.choice(possible_labels)

    # Save prediction to database
    success, error = insert_prediction(user_id, file.filename, public_url, label)
    if not success:
        return jsonify({"error": error}), 500

    return jsonify({"label": label, "file_url": public_url})


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

    try:
        db_res = sb.table(TABLE_NAME).select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return jsonify(db_res.data)
    except Exception as e:
        logger.error(f"Exception during history fetch: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500

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
    try:
        # Fetch prediction record
        fetch_res = sb.table(TABLE_NAME).select("file_url").eq("id", pred_id).maybe_single().execute()
        record = fetch_res.data
        if not record:
            return jsonify({"error": "Prediction not found"}), 404

        # Parse file path
        file_url = record.get("file_url")
        file_path = file_url.split(f"/{BUCKET_NAME}/")[1] if f"/{BUCKET_NAME}/" in file_url else None

        # Remove file from storage
        if file_path:
            remove_res = sb.storage.from_(BUCKET_NAME).remove([file_path])
            if remove_res.get("error"):
                logger.error(f"Failed to delete file from storage: {remove_res['error']}")
                return jsonify({"error": "Failed to delete file from storage"}), 500

        # Delete record from database
        delete_res = sb.table(TABLE_NAME).delete().eq("id", pred_id).execute()
        if delete_res.error:
            logger.error(f"Failed to delete prediction record: {delete_res.error}")
            return jsonify({"error": "Failed to delete prediction record"}), 500

        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Exception during deletion: {e}")
        return jsonify({"error": "Failed to delete prediction"}), 500

if __name__ == '__main__':
    """
    Run the Flask app locally or on Render.
    Environment Variables:
    - SUPABASE_URL: Your Supabase project URL.
    - SUPABASE_KEY: Your Supabase service key.
    """
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)