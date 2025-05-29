from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite for demo; replace with your DB URL for production (e.g., PostgreSQL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./file_sharing.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# If you want to create tables on startup, do it at the bottom of this file:
# from models import Base
# Base.metadata.create_all(bind=engine)