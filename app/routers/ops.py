from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.auth import get_current_user_ops
import shutil
import os

router = APIRouter()

ALLOWED_EXT = ['pptx', 'docx', 'xlsx']

@router.post("/login")
def login_ops():
    # standard login, returns JWT for ops user
    pass

@router.post("/upload-file")
def upload_file(file: UploadFile = File(...), user=Depends(get_current_user_ops)):
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Invalid file type")
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    # Save file logic
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # TODO: Add DB record for uploaded file
    return {"message": "File Uploaded"}