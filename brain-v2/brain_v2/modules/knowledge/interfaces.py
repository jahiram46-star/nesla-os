from abc import ABC, abstractmethod
from typing import List
from brain_v2.modules.knowledge.schemas import KnowledgeDocument

class IKnowledgeLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> List[KnowledgeDocument]:
        pass

class IKnowledgeParser(ABC):
    @abstractmethod
    def parse(self, raw_content: str) -> str:
        pass

class IKnowledgeIndexer(ABC):
    @abstractmethod
    def add_documents(self, docs: List[KnowledgeDocument]):
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 5) -> List[KnowledgeDocument]:
        pass