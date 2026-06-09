from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IWorkspaceManager(ABC):
    """Interface for managing the MRM Workspace environment."""
    
    @abstractmethod
    async def file_operation(self, op_type: str, path: str, content: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def terminal_execute(self, command: str, work_dir: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def git_operation(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def project_lifecycle(self, action: str, project_id: str) -> Dict[str, Any]:
        pass

class IBuildSystem(ABC):
    """Interface for interacting with compilers and build tools."""
    @abstractmethod
    async def run_build(self, config: Dict[str, Any]) -> Dict[str, Any]:
        pass

class IDebugSystem(ABC):
    """Interface for interacting with debuggers."""
    @abstractmethod
    async def start_debug_session(self, target: str) -> str:
        pass