from typing import List, Optional
from sqlalchemy.orm import Session
from brain_v2.modules.memory.models import MemoryEntry
from brain_v2.modules.memory.schemas import MemoryCreate, MemoryType

class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schema: MemoryCreate) -> MemoryEntry:
        db_obj = MemoryEntry(**schema.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_by_id(self, memory_id: str) -> Optional[MemoryEntry]:
        return self.db.query(MemoryEntry).filter(MemoryEntry.id == memory_id).first()

    def search(self, query: str, m_type: Optional[MemoryType] = None, context_id: Optional[str] = None, limit: int = 10) -> List[MemoryEntry]:
        filters = []
        if m_type:
            filters.append(MemoryEntry.memory_type == m_type)
        if context_id:
            filters.append(MemoryEntry.context_id == context_id)
        
        return self.db.query(MemoryEntry).filter(
            *filters,
            MemoryEntry.content.ilike(f"%{query}%")
        ).order_by(MemoryEntry.created_at.desc()).limit(limit).all()

    def delete(self, memory_id: str) -> bool:
        obj = self.get_by_id(memory_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False