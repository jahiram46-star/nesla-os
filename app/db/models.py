from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.database import Base


class AppStatus(Base):
    __tablename__ = "app_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False, default="NESLA AI")
    status = Column(String(length=50), nullable=False, default="healthy")


class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    ai_response = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
