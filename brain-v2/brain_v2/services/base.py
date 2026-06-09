from abc import ABC, abstractmethod
from pydantic import BaseModel
from brain_v2.schemas.module import ModuleStatusResponse

class ModuleMetadata(BaseModel):
    """
    Standardized metadata used for discovery and logging within the Brain.
    """
    key: str
    name: str
    description: str

class BaseModuleService(ABC):
    """
    The blueprint for all Brain V2 engine services.
    Ensures every engine provides health/status information and basic metadata.
    """
    metadata: ModuleMetadata

    @abstractmethod
    async def status(self) -> ModuleStatusResponse:
        """
        Returns the operational status of the module.
        Must be implemented by all sub-engines.
        """
        raise NotImplementedError("Subclasses must implement status()")

    def __repr__(self):
        return f"<{self.__class__.__name__}(key={self.metadata.key})>"