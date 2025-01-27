import os

# Load environment variables for local development
from dotenv import load_dotenv

load_dotenv()


class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    BUCKET_NAME = "images"
    TABLE_NAME = "predictions"
    ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "https://resonant-chaja-d637bc.netlify.app",
    ]
