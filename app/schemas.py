from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# ---------- User Schemas ----------

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str  # constr(min_length=6) is not supported in Pydantic v2, use validator if needed

class UserOut(UserBase):
    id: int
    is_ops: bool
    is_verified: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ---------- File Schemas ----------

class FileOut(BaseModel):
    id: int
    filename: str
    uploaded_by_id: int

    class Config:
        from_attributes = True

# ---------- Download Link Schemas ----------

class DownloadLinkOut(BaseModel):
    download_link: str
    message: str

# ---------- Token Schemas ----------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    is_ops: Optional[bool] = None
    is_verified: Optional[bool] = None