from typing import Optional, Any, Dict
from pydantic import BaseModel

class ModuleStatusResponse(BaseModel):
    """
    Shared response schema for module health checks.
    """
    key: str
    name: str
    status: str  # e.g., "active", "degraded", "offline"
    description: str
    uptime_seconds: Optional[int] = None
    error_count: int = 0
    last_error: Optional[str] = None
    metrics: Dict[str, Any] = {}