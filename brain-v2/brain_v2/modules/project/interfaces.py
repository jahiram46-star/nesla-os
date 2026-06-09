from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class ProjectAnalyzer(ABC):
    """Interface for analyzing project structure and health."""
    
    @abstractmethod
    async def analyze_structure(self, path: str, depth: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def evaluate_health(self, project_id: str) -> str:
        pass