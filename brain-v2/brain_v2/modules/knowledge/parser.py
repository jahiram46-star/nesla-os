import re
from brain_v2.modules.knowledge.interfaces import IKnowledgeParser

class MarkdownParser(IKnowledgeParser):
    def parse(self, raw_content: str) -> str:
        # Remove markdown syntax to get clean text for indexing
        # This is a basic implementation; can be expanded with libraries like 'marko'
        text = re.sub(r'#+\s?', '', raw_content)  # Headers
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
        text = re.sub(r'[*_~`]', '', text)  # Basic formatting
        return text.strip()