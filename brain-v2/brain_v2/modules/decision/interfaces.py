from abc import ABC, abstractmethod
from typing import List, Dict
from brain_v2.modules.decision.schemas import DecisionRequest, DecisionResult

class IDecisionEvaluator(ABC):
    @abstractmethod
    def score_action(self, action: str, request: DecisionRequest) -> float:
        pass

class IGoalAligner(ABC):
    @abstractmethod
    def check_alignment(self, action: str, goals: List[str]) -> Dict[str, float]:
        pass