from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_ops = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    uploaded_by_id = Column(Integer, ForeignKey('users.id'))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class DownloadLink(Base):
    __tablename__ = "download_links"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    client_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, unique=True)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime)