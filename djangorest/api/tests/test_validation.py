import pytest

from api.models import User

from .conftest import USERS_URL

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "payload, bad_field",
    [
        ({"name": "Peter", "age": -1}, "age"),
        ({"name": "Peter", "age": 151}, "age"),
        ({"name": "Peter", "age": "abc"}, "age"),
        ({"name": "Peter"}, "age"),
        ({"age": 25}, "name"),
        ({"name": "   ", "age": 25}, "name"),
        ({"name": "12345", "age": 25}, "name"),
        ({"name": "x" * 101, "age": 25}, "name"),
    ],
)
def test_invalid_payload_rejected(auth_client, payload, bad_field):
    resp = auth_client.post(USERS_URL, payload, format="json")

    assert resp.status_code == 400
    assert bad_field in resp.json()
    assert User.objects.count() == 0


@pytest.mark.parametrize("age", [0, 150])
def test_age_boundaries_accepted(auth_client, age):
    resp = auth_client.post(USERS_URL, {"name": "Edge", "age": age}, format="json")

    assert resp.status_code == 201


def test_name_whitespace_is_trimmed(auth_client):
    resp = auth_client.post(USERS_URL, {"name": "  Peter  ", "age": 25}, format="json")

    assert resp.status_code == 201
    assert resp.json()["name"] == "Peter"


def test_id_is_read_only(auth_client):
    resp = auth_client.post(USERS_URL, {"id": 999, "name": "Peter", "age": 25}, format="json")

    assert resp.status_code == 201
    assert resp.json()["id"] != 999
    assert not User.objects.filter(pk=999).exists()
