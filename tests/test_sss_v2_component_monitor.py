import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.sss_v2.schemas import ComponentHealthCheckCreate, ComponentStatus
from app.sss_v2.services.component_monitor import ComponentMonitorService


class TestComponentMonitorService(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()
        self.service = ComponentMonitorService(self.session)

    def tearDown(self) -> None:
        self.session.close()

    def test_online_component_does_not_create_incident_or_alert(self) -> None:
        result = self.service.record_check(
            ComponentHealthCheckCreate(
                component="Knowledge",
                status=ComponentStatus.online,
                response_time_ms=12,
                message="Knowledge is responding.",
            )
        )

        self.assertFalse(result.failure_detected)
        self.assertIsNone(result.incident)
        self.assertIsNone(result.admin_alert)

    def test_failed_component_creates_incident_and_admin_alert_without_ivr(self) -> None:
        result = self.service.record_check(
            ComponentHealthCheckCreate(
                component="Memory",
                status=ComponentStatus.failed,
                message="Memory health check failed.",
                details={"reason": "connection refused"},
            )
        )

        self.assertTrue(result.failure_detected)
        self.assertEqual(result.incident.category, "component_failure")
        self.assertTrue(result.incident.requires_admin_alert)
        self.assertFalse(result.incident.requires_ivr_call)
        self.assertEqual(result.admin_alert.status, "pending")

    def test_latest_checks_returns_latest_status_for_each_component(self) -> None:
        self.service.record_check(
            ComponentHealthCheckCreate(
                component="Documents",
                status=ComponentStatus.failed,
                message="Documents failed.",
            )
        )
        self.service.record_check(
            ComponentHealthCheckCreate(
                component="Documents",
                status=ComponentStatus.online,
                message="Documents recovered.",
            )
        )

        latest = self.service.latest_checks()

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0].status, ComponentStatus.online.value)


if __name__ == "__main__":
    unittest.main()
