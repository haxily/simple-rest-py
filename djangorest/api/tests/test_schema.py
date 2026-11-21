import pytest
import yaml

pytestmark = pytest.mark.django_db


def test_schema_lists_user_endpoints(api_client):
    resp = api_client.get("/api/schema/")

    assert resp.status_code == 200
    schema = yaml.safe_load(resp.content)
    assert "/api/users/" in schema["paths"]
    assert "/api/users/{id}/" in schema["paths"]
    assert "jwtAuth" in schema["components"]["securitySchemes"]


@pytest.mark.parametrize("url", ["/api/docs/", "/api/redoc/"])
def test_docs_pages_render(api_client, url):
    assert api_client.get(url).status_code == 200
