from typing import Generator

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import Knowledge, SessionLocal
from app.schemas.knowledge import KnowledgeCreate, KnowledgeRead

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_knowledge(knowledge: KnowledgeCreate, db: Session = Depends(get_db)) -> Knowledge:
    db_knowledge = Knowledge(**knowledge.dict())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


@router.get("", response_model=list[KnowledgeRead])
def read_knowledge(db: Session = Depends(get_db)) -> list[Knowledge]:
    return db.query(Knowledge).order_by(Knowledge.created_at.desc()).all()
