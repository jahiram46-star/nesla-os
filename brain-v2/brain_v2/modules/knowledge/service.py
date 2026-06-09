from typing import List, Optional
from brain_v2.services.base import BaseModuleService, ModuleMetadata
from brain_v2.schemas.module import ModuleStatusResponse
from brain_v2.modules.knowledge.schemas import KnowledgeDocument, KnowledgeSearchResponse, KnowledgeIngestResponse
from brain_v2.modules.knowledge.interfaces import IKnowledgeLoader, IKnowledgeIndexer
from brain_v2.modules.knowledge.loader import LocalMarkdownLoader # Default loader
from brain_v2.core.config import settings # Import settings
import os

class KnowledgeEngineService(BaseModuleService):
    metadata = ModuleMetadata(
        key="knowledge",
        name="Knowledge Engine",
        description="Information search and retrieval engine.",
    )

    def __init__(self, loader: Optional[IKnowledgeLoader] = None, indexer: Optional[IKnowledgeIndexer] = None):
        self.source_dir = settings.KNOWLEDGE_SOURCE_DIR
        os.makedirs(self.source_dir, exist_ok=True)
        self.loader = loader or LocalMarkdownLoader()
        # In a real scenario, an actual indexer (e.g., with a vector DB) would be used
        # For now, we'll simulate an in-memory index
        self._documents: List[KnowledgeDocument] = []

    async def status(self) -> ModuleStatusResponse:
        return ModuleStatusResponse(
            key=self.metadata.key,
            name=self.metadata.name,
            status="active",
            description=self.metadata.description
        )
    async def ingest_local_files(self) -> KnowledgeIngestResponse:
        """Loads and indexes documents from the local source directory."""
        new_docs = self.loader.load(self.source_dir)
        processed_count = 0
        for doc in new_docs:
            # Simple deduplication for this mock
            if not any(d.title == doc.title and d.content == doc.content for d in self._documents):
                self._documents.append(doc)
                processed_count += 1
        return KnowledgeIngestResponse(
            success=True,
            processed_files=processed_count,
            message=f"Successfully ingested {processed_count} new documents."
        )

    async def search(self, query: str, limit: int = 5) -> KnowledgeSearchResponse:
        """Performs a basic keyword search on ingested documents."""
        results = [
            doc for doc in self._documents
            if query.lower() in doc.title.lower() or query.lower() in doc.content.lower()
        ]
        # Sort by relevance (simple: just return first 'limit' matches)
        limited_results = results[:limit]
        return KnowledgeSearchResponse(results=limited_results, count=len(limited_results))