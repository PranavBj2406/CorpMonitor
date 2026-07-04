from fastapi import APIRouter, UploadFile, File, HTTPException
import hashlib
from app.services.pipeline_services import process_zip

router = APIRouter()


@router.post("/extract")
async def extract_documents(
    zip_file: UploadFile = File(...)
):
    """
    Upload a ZIP archive containing PDFs.
    """
    content = await zip_file.read()

    print("=" * 80)
    print("Filename:", zip_file.filename)
    print("Size:", len(content))
    print("SHA256:", hashlib.sha256(content).hexdigest())
    print("=" * 80)

    if not zip_file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    if not zip_file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are allowed."
        )

    result = await process_zip(zip_file)

    return {
        "status": "success",
        "data": result,
    }