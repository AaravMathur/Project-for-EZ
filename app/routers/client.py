from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import FileResponse
from app.auth import get_current_user_client, get_password_hash, authenticate_user, create_access_token
from app.utils import create_verification_token, create_download_token, verify_download_token
from app.models import File, DownloadLink, User
from app.database import get_db
from sqlalchemy.orm import Session
import datetime

router = APIRouter()
@router.post("/signup")
def signup(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, is_ops=False, is_verified=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_verification_token(email)
    verification_url = f"http://127.0.0.1:8080/client/email-verify?token={token}"
    print({"verification_url": verification_url})  # Print output to console
    # send_email(email, verification_url)
    return {"verification_url": verification_url}

@router.get("/signup")
def signup_get():
    return {"message": "This endpoint supports both POST (to register) and GET (to show this message). To register, send a POST request with 'email' and 'password' as form data."}

@router.get("/email-verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = verify_download_token(token)
    email = payload.get("email")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified"}

@router.post("/login")
def login_client(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password, is_ops=False)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = create_access_token({"user_id": user.id, "is_ops": user.is_ops, "is_verified": user.is_verified})
    print({"access_token": access_token, "token_type": "bearer"})  # Print output to console
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/files")
def list_files(user=Depends(get_current_user_client), db: Session = Depends(get_db)):
    return db.query(File).all()

@router.post("/generate-download-link/{file_id}")
def generate_download_link(file_id: int, user=Depends(get_current_user_client), db: Session = Depends(get_db)):
    token = create_download_token(file_id, user.id)
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    link = DownloadLink(file_id=file_id, client_id=user.id, token=token, expires_at=expires_at)
    db.add(link)
    db.commit()
    return {"download_link": f"http://127.0.0.1:8080/client/download-file/{token}", "message": "success"}

@router.get("/download-file/{token}")
def download_file(token: str, user=Depends(get_current_user_client), db: Session = Depends(get_db)):
    link = db.query(DownloadLink).filter(DownloadLink.token == token, DownloadLink.client_id == user.id).first()
    if not link or link.is_used or link.expires_at < datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=403, detail="Invalid or expired link")
    link.is_used = True
    db.commit()
    file = db.query(File).filter(File.id == link.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(f"uploads/{file.filename}")

@router.post("/signup/test")
def signup_test(db: Session = Depends(get_db)):
    import random
    import string
    email = f"testuser_{random.randint(1000,9999)}@example.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    # Check if user already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, is_ops=False, is_verified=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_verification_token(email)
    verification_url = f"http://127.0.0.1:8080/client/email-verify?token={token}"
    print({"email": email, "password": password, "verification_url": verification_url})
    return {"email": email, "password": password, "verification_url": verification_url}