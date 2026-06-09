from abc import ABC, abstractmethod
from typing import Any, Dict, List
from brain_v2.modules.execution.schemas import ExecutionResult

class ExecutionHandler(ABC):
    """Base interface for all execution handlers (Command, Task, Project)."""
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> ExecutionResult:
        """Core execution logic."""
        pass

    @abstractmethod
    async def validate(self, result: ExecutionResult) -> bool:
        """Post-execution validation."""
        pass

    @abstractmethod
    async def rollback(self, execution_id: str) -> bool:
        """Undo changes if execution fails."""
        pass

class WorkflowOrchestrator(ABC):
    """Interface for managing complex multi-step execution pipelines."""
    
    @abstractmethod
    async def run_pipeline(self, steps: List[Dict[str, Any]]) -> List[ExecutionResult]:
        """Execute a sequence of tasks with dependency management."""
        pass

class ProcessManager(ABC):
    """Interface for OS-level process and command management."""
    
    @abstractmethod
    async def spawn(self, command: str, args: List[str], env: Dict[str, str]) -> Dict[str, Any]:
        """Execute a shell command or binary."""
        pass