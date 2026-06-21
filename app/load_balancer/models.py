from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String, Text, func

from app.db.database import Base


class LoadBalancerServer(Base):
    __tablename__ = "load_balancer_servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), nullable=False, unique=True, index=True)
    host = Column(String(length=255), nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String(length=16), nullable=False, default="http")
    status = Column(String(length=32), nullable=False, default="active", index=True)
    weight = Column(Integer, nullable=False, default=1)
    max_modules = Column(Integer, nullable=False, default=8)
    capabilities = Column(JSON, nullable=False, default=list)
    rules = Column(JSON, nullable=False, default=dict)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ModulePlacement(Base):
    __tablename__ = "load_balancer_module_placements"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(length=128), nullable=False, index=True)
    server_id = Column(Integer, nullable=False, index=True)
    route_prefix = Column(String(length=128), nullable=False)
    priority = Column(Integer, nullable=False, default=1)
    enabled = Column(Boolean, nullable=False, default=True, index=True)
    health_path = Column(String(length=128), nullable=False, default="/health")
    load_score = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
