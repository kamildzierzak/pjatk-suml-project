import time
import logging

from supabase import Client
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def insert_prediction(sb: Client, table_name: str, user_id: str, filename: str, file_url: str, label: str):
    """Insert a prediction record into the database."""
    try:
        prediction_data = {
            "user_id": user_id,
            "filename": filename,
            "file_url": file_url,
            "label": label,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        db_res = sb.table(table_name).insert(prediction_data).execute()

        if not db_res:
            logger.error("Prediction insertion failed")
            return False, "Failed to save prediction"

        return True, None
    except Exception as e:
        logger.error(f"Exception during prediction insertion: {e}")
        return False, "Internal server error during prediction insertion"

# services/database.py
def fetch_history(sb: Client, table_name: str, user_id: str):
    """Fetch prediction history for a specific user."""
    try:
        db_res = sb.table(table_name).select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

        if not db_res.data:
            return [], None

        return db_res.data, None
    except Exception as e:
        logger.error(f"Exception during history fetch: {e}")
        return None, "Failed to fetch history"

def delete_prediction(sb: Client, table_name: str, bucket_name: str, pred_id: int):
    """Delete a prediction record and associated file."""
    try:
        # Fetch the prediction record
        fetch_res = sb.table(table_name).select("file_url").eq("id", pred_id).maybe_single().execute()

        if not fetch_res.data:
            return None, "Prediction not found"

        record = fetch_res.data
        file_url = record.get("file_url")
        if not file_url:
            return None, "File URL not found"

        parsed_url = urlparse(file_url)
        path = parsed_url.path
        file_path = path.split(f"/{bucket_name}/")[1] if f"/{bucket_name}/" in path else None

        if not file_path:
            return None, "Invalid file path"

        # Remove file from storage
        remove_res = sb.storage.from_(bucket_name).remove([file_path])
        logger.debug(f"Remove response: {remove_res}")

        # Delete record from database
        delete_res = sb.table(table_name).delete().eq("id", pred_id).execute()
        if not delete_res.data or len(delete_res.data) == 0:
            logger.error(f"Failed to delete prediction record: {delete_res}")
            return None, "Failed to delete prediction record"

        logger.info(f"Successfully deleted prediction record {pred_id}")
        return {"success": True}, None
    except Exception as e:
        logger.error(f"Exception during deletion: {e}")
        return None, "Failed to delete prediction"