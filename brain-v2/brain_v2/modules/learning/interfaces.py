from abc import ABC, abstractmethod
from typing import Any, Dict, List
from brain_v2.modules.learning.schemas import LearningResult

class OutcomeAnalyzer(ABC):
    """Base interface for analyzing the outcomes of system actions."""
    
    @abstractmethod
    async def analyze(self, source_id: str, data: Dict[str, Any]) -> LearningResult:
        """Perform deep analysis on execution or decision data."""
        pass

class PatternDetector(ABC):
    """Interface for identifying recurring sequences in historical data."""
    
    @abstractmethod
    async def detect_patterns(self, history: List[Dict[str, Any]]) -> List[str]:
        """Identify successes or failure patterns."""
        pass

class FeedbackProcessor(ABC):
    """Interface for processing explicit or implicit feedback loops."""
    
    @abstractmethod
    async def process_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Update system weights or knowledge based on feedback."""
        pass