from fastapi.testclient import TestClient

from supply_chain.api.main import create_app
from supply_chain.core.config import Settings, get_settings


def test_health_and_status_work_without_hopsworks_and_do_not_expose_secrets():
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None,
        hopsworks_host="",
        hopsworks_api_key="private-test-key",
    )
    with TestClient(app) as client:
        assert client.get("/health/live").json() == {"status": "ok"}
        assert client.get("/health/ready").json() == {"status": "ready"}
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json()["feature_store"] == {
            "provider": "Hopsworks",
            "configured": False,
            "connection": "not_checked",
        }
        assert "private-test-key" not in response.text
        assert {p["name"] for p in response.json()["pipelines"]} == {"smoke", "feature_snapshot"}
