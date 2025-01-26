import time
import logging
from supabase import Client

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
        file_path = file_url.split(f"/{bucket_name}/")[1] if f"/{bucket_name}/" in file_url else None

        # Remove file from storage
        if file_path:
            sb.storage.from_(bucket_name).remove([file_path])
            logger.info(f"Removed file: {file_path}")

        # Delete record from database
        delete_res = sb.table(table_name).delete().eq("id", pred_id).execute()

        if not delete_res.data or len(delete_res.data) == 0:
            return None, "Failed to delete prediction record"

        return {"success": True}, None
    except Exception as e:
        logger.error(f"Exception during deletion: {e}")
        return None, "Failed to delete prediction"