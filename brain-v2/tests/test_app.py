from fastapi.testclient import TestClient

from brain_v2.main import create_app


def test_app_metadata():
    app = create_app()
    assert app.title == "NESLA Brain V2"
