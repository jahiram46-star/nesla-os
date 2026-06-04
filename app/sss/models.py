from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.database import Base


class SystemEvent(Base):
    __tablename__ = "system_events"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(length=100), nullable=False)
    event_type = Column(String(length=50), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
