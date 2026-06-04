from typing import Generator

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import Memory, SessionLocal
from app.schemas.memory import MemoryCreate, MemoryRead

router = APIRouter(prefix="/memory", tags=["memory"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=MemoryRead, status_code=status.HTTP_201_CREATED)
def create_memory(memory: MemoryCreate, db: Session = Depends(get_db)) -> Memory:
    db_memory = Memory(**memory.dict())
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory


@router.get("/test")
def memory_test() -> dict:
    return {"message": "memory module working"}


@router.get("", response_model=list[MemoryRead])
def read_memories(db: Session = Depends(get_db)) -> list[Memory]:
    return db.query(Memory).order_by(Memory.created_at.desc()).all()
