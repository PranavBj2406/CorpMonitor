import shutil
import tempfile
import zipfile
from pathlib import Path
import logging
from app.core.config import settings
logger = logging.getLogger(__name__)
import time

from fastapi import HTTPException, UploadFile

from src.pipeline import run_pipeline


async def process_zip(zip_file: UploadFile):
    """
    Process an uploaded ZIP archive containing PDF files.
    """
    if not zip_file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
    )
    zip_file.file.seek(0, 2)
    file_size = zip_file.file.tell()
    zip_file.file.seek(0)
    logger.info(f"Uploaded file size: {file_size / (1024 * 1024):.2f} MB")
    if file_size > settings.MAX_UPLOAD_SIZE:
        logger.warning(
            f"Upload rejected. File size {file_size} exceeds limit."
        )
        raise HTTPException(
        status_code=413,
        detail=f"Maximum upload size is {settings.MAX_UPLOAD_SIZE // (1024 * 1024)} MB."
    )

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_dir = Path(temp_dir)

        # Save uploaded ZIP
        zip_path = temp_dir / zip_file.filename
        logger.info(f"Received ZIP upload: {zip_file.filename}")

        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(zip_file.file, buffer)
            logger.info(f"Saved ZIP to temporary location: {zip_path}")

        # Extract ZIP
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                logger.info("Extracting ZIP archive...")
                zip_ref.extractall(temp_dir)

        except zipfile.BadZipFile:
            logger.error("Uploaded file is not a valid ZIP archive.")

            raise HTTPException(
                status_code=400,
                detail="Invalid ZIP file."
            )
        logger.info("ZIP extracted successfully.")

        # Find PDFs recursively
        pdf_files = list(temp_dir.rglob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF(s).")

        if not pdf_files:
            raise HTTPException(
                status_code=400,
                detail="No PDF files found in uploaded ZIP."
            )

        # Run ETL pipeline
        try:
            logger.info("Starting ETL pipeline...")
            start=time.perf_counter()
            result = run_pipeline(
                input_dir=temp_dir,
                output_file=None
            )
            end = time.perf_counter()
            logger.info("ETL pipeline completed successfully.")
            logger.info(f"Pipeline completed in {end - start:.2f} seconds")
        
        except Exception:
            logger.exception("Pipeline execution failed.")
            raise HTTPException(
            status_code=500,
            detail="Pipeline execution failed."
            )

        return result