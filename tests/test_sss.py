from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sss_status() -> None:
    response = client.get("/sss/status")
    assert response.status_code == 200
    assert response.json() == {"module": "SSS", "status": "active"}


def test_sss_modules() -> None:
    response = client.get("/sss/modules")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "Brain", "status": "online"},
        {"name": "Memory", "status": "online"},
        {"name": "Knowledge", "status": "online"},
        {"name": "Documents", "status": "online"},
    ]


def test_sss_event_crud() -> None:
    payload = {
        "module_name": "Brain",
        "event_type": "warning",
        "message": "Brain response delay detected",
    }
    post_response = client.post("/sss/event", json=payload)
    assert post_response.status_code == 201
    created_event = post_response.json()
    assert created_event["module_name"] == payload["module_name"]
    assert created_event["event_type"] == payload["event_type"]
    assert created_event["message"] == payload["message"]
    assert "id" in created_event
    assert "created_at" in created_event

    list_response = client.get("/sss/events")
    assert list_response.status_code == 200
    events = list_response.json()
    assert any(event["id"] == created_event["id"] for event in events)
