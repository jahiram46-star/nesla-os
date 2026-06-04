from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite URL (file-based, relative to project root)
DATABASE_URL = "sqlite:///./nesla.db"

# For SQLite, disable same-thread check for SQLAlchemy when using FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db() -> None:
    """Create database tables. Call at startup if needed."""
    Base.metadata.create_all(bind=engine)
