from pathlib import Path
from typing import List
from brain_v2.modules.knowledge.interfaces import IKnowledgeLoader
from brain_v2.modules.knowledge.schemas import KnowledgeDocument

class LocalMarkdownLoader(IKnowledgeLoader):
    def load(self, source: str) -> List[KnowledgeDocument]:
        path = Path(source)
        if not path.exists():
            return []

        documents = []
        for file_path in path.glob("**/*.md"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(
                    KnowledgeDocument(
                        title=file_path.name,
                        content=content,
                        metadata={"path": str(file_path)}
                    )
                )
        return documents