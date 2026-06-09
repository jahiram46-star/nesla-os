import pytest
from brain_v2.modules.knowledge.service import KnowledgeEngineService
from brain_v2.modules.knowledge.parser import MarkdownParser

def test_markdown_parser():
    parser = MarkdownParser()
    raw = "# Hello\nThis is [Nesla](https://nesla.ai) AI **Logic**."
    expected = "Hello\nThis is Nesla AI Logic."
    assert parser.parse(raw) == expected

@pytest.mark.asyncio
async def test_knowledge_search_empty():
    service = KnowledgeEngineService()
    response = await service.search("anything")
    assert response.count == 0
    assert len(response.results) == 0

@pytest.mark.asyncio
async def test_knowledge_ingestion_mock(tmp_path):
    service = KnowledgeEngineService()
    service.source_dir = str(tmp_path)
    
    # Create dummy md
    (tmp_path / "test.md").write_text("# Test Title\nImportant knowledge here.")
    
    res = await service.ingest_local_files()
    assert res.processed_files == 1