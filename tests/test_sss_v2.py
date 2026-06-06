from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sss_v2_status() -> None:
    response = client.get("/sss/v2/status")

    assert response.status_code == 200
    assert response.json()["module"] == "SSS V2"
    assert response.json()["telephony_provider_configured"] is False


def test_critical_signal_creates_alert_and_ivr_workflow() -> None:
    response = client.post(
        "/sss/v2/security/signals",
        json={
            "source": "authentication_gateway",
            "signal_type": "credential_attack",
            "severity": "critical",
            "title": "Credential attack detected",
            "description": "Repeated privileged login failures detected.",
            "details": {"attempts": 25},
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["incident"]["requires_admin_alert"] is True
    assert body["incident"]["requires_ivr_call"] is True
    assert body["admin_alert"]["status"] == "pending"
    assert body["ivr_workflow"]["status"] == "queued"
    assert body["ivr_workflow"]["provider"] is None


def test_healthy_project_snapshot_does_not_create_incident() -> None:
    response = client.post(
        "/sss/v2/health/snapshots",
        json={
            "project_name": "NESLA OS",
            "component": "API",
            "status": "healthy",
            "health_score": 99.0,
            "summary": "All checks passed.",
            "metrics": {"latency_ms": 12},
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["incident"] is None
    assert body["admin_alert"] is None
    assert body["ivr_workflow"] is None


def test_failed_component_creates_incident_and_admin_alert_without_ivr() -> None:
    response = client.post(
        "/sss/v2/components/checks",
        json={
            "component": "Knowledge",
            "status": "failed",
            "message": "Knowledge component is unavailable.",
            "details": {"check": "heartbeat"},
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["failure_detected"] is True
    assert body["incident"]["category"] == "component_failure"
    assert body["incident"]["requires_ivr_call"] is False
    assert body["admin_alert"]["status"] == "pending"
