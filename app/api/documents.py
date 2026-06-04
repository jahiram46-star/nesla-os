from pathlib import Path
from typing import Generator

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.db import Knowledge, SessionLocal
from app.schemas.knowledge import KnowledgeRead, KnowledgeCreate

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ALLOWED_EXT = {".txt", ".md"}


@router.post("/upload", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)) -> KnowledgeRead:
    filename = Path(file.filename)
    if filename.suffix.lower() not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    safe_name = filename.name
    dest = UPLOAD_DIR / safe_name
    # avoid overwrite
    if dest.exists():
        stem = filename.stem
        suffix = filename.suffix
        count = 1
        while True:
            new_name = f"{stem}_{count}{suffix}"
            new_dest = UPLOAD_DIR / new_name
            if not new_dest.exists():
                dest = new_dest
                safe_name = new_name
                break
            count += 1

    content_bytes = await file.read()
    try:
        content = content_bytes.decode("utf-8")
    except Exception:
        content = content_bytes.decode("utf-8", errors="replace")

    # save file to uploads
    dest.write_bytes(content.encode("utf-8"))

    # save to Knowledge table
    db_entry = Knowledge(title=safe_name, content=content)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return db_entry


@router.get("", response_model=list[KnowledgeRead])
def list_documents(db: Session = Depends(get_db)) -> list[Knowledge]:
    return db.query(Knowledge).order_by(Knowledge.created_at.desc()).all()
