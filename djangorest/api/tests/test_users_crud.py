import pytest

from api.models import User

from .conftest import USERS_URL, detail_url

pytestmark = pytest.mark.django_db


def test_list_is_public_and_paginated(api_client, make_user):
    make_user("Peter", 25)
    make_user("Bob", 40)

    resp = api_client.get(USERS_URL)

    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 2
    assert {"next", "previous", "results"} <= body.keys()
    assert [u["name"] for u in body["results"]] == ["Peter", "Bob"]


def test_create(auth_client):
    resp = auth_client.post(USERS_URL, {"name": "Peter", "age": 25}, format="json")

    assert resp.status_code == 201
    assert resp.json()["name"] == "Peter"
    assert User.objects.filter(name="Peter", age=25).exists()


def test_retrieve(api_client, make_user):
    user = make_user()

    resp = api_client.get(detail_url(user.pk))

    assert resp.status_code == 200
    assert resp.json() == {"id": user.pk, "name": "Peter", "age": 25}


def test_retrieve_missing_returns_404(api_client):
    assert api_client.get(detail_url(9999)).status_code == 404


def test_put_replaces(auth_client, make_user):
    user = make_user()

    resp = auth_client.put(detail_url(user.pk), {"name": "Bob", "age": 30}, format="json")

    assert resp.status_code == 200
    user.refresh_from_db()
    assert (user.name, user.age) == ("Bob", 30)


def test_put_requires_all_fields(auth_client, make_user):
    user = make_user()

    resp = auth_client.put(detail_url(user.pk), {"age": 30}, format="json")

    assert resp.status_code == 400
    assert "name" in resp.json()


def test_patch_updates_partially(auth_client, make_user):
    user = make_user()

    resp = auth_client.patch(detail_url(user.pk), {"age": 31}, format="json")

    assert resp.status_code == 200
    user.refresh_from_db()
    assert (user.name, user.age) == ("Peter", 31)


def test_delete(auth_client, make_user):
    user = make_user()

    resp = auth_client.delete(detail_url(user.pk))

    assert resp.status_code == 204
    assert not User.objects.filter(pk=user.pk).exists()


def test_str_is_name(make_user):
    assert str(make_user("Peter")) == "Peter"
