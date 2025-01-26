import re
import time
import logging

from werkzeug.utils import secure_filename
from supabase import Client

logger = logging.getLogger(__name__)

def sanitize_user_id(user_id):
    """Sanitize user_id to remove invalid characters for filenames."""
    return re.sub(r"[^a-zA-Z0-9_-]", "_", user_id)

def upload_file_to_storage(sb: Client, bucket_name: str, file, user_id: str):
    """Upload a file to Supabase Storage and return its public URL."""
    try:
        # Sanitize user_id
        sanitized_user_id = sanitize_user_id(user_id)

        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_name = f"{sanitized_user_id}_{int(time.time())}_{original_filename}"

        # Read file content
        file_bytes = file.read()

        # Upload file to Supabase Storage
        upload_res = sb.storage.from_(bucket_name).upload(
            unique_name, file_bytes, {"content-type": file.mimetype}
        )

        if not upload_res:
            logger.error("File upload failed: No response received")
            return None, "File upload failed"

        # Get public URL
        public_url_res = sb.storage.from_(bucket_name).get_public_url(unique_name)

        if not public_url_res:
            logger.error("Failed to get public URL")
            return None, "Failed to get public URL"

        return public_url_res, None
    except Exception as e:
        logger.error(f"Exception during file upload: {e}")
        return None, "Internal server error during file upload"
