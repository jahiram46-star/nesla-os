from abc import ABC, abstractmethod
from typing import Optional

from app.sss_v2.schemas import (
    AdminAlertDispatch,
    IvrCallDispatch,
    SecuritySignalCreate,
    ThreatAssessment,
)


class ThreatDetector(ABC):
    """Contract for pluggable threat-detection engines."""

    @abstractmethod
    def assess(self, signal: SecuritySignalCreate) -> ThreatAssessment:
        """Assess a security signal without performing response actions."""


class AdminAlertGateway(ABC):
    """Contract for delivering alerts to the NESLA Admin Panel."""

    @abstractmethod
    def send(self, alert: AdminAlertDispatch) -> Optional[str]:
        """Deliver an alert and return an optional provider reference."""


class IvrCallingGateway(ABC):
    """Contract for telephony providers. No provider is configured in V2 foundation."""

    @abstractmethod
    def trigger(self, workflow: IvrCallDispatch) -> Optional[str]:
        """Start an IVR call and return an optional provider reference."""
