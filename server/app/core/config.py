from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    # ==========================
    # API
    # ==========================
    API_TITLE = "Director Change Extraction API"
    API_VERSION = "1.0.0"

    # ==========================
    # Upload Configuration
    # ==========================
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB
    ALLOWED_FILE_EXTENSION = ".zip"

    # ==========================
    # Temporary Storage
    # ==========================
    TEMP_DIRECTORY = Path("temp")

    # ==========================
    # Gemini
    # ==========================
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # ==========================
    # CORS
    # ==========================
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
    ]


settings = Settings()