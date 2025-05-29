from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import File
from schemas import FileOut
from typing import List

router = APIRouter()

@router.get("/files", response_model=List[FileOut])
def list_all_files(db: Session = Depends(get_db)):
    """
    List all uploaded files (for admin/testing purposes).
    Not intended for production, restrict access as needed.
    """
    return db.query(File).all()