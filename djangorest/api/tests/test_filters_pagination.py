import pytest

from .conftest import USERS_URL

pytestmark = pytest.mark.django_db


@pytest.fixture
def people(make_user):
    for name, age in [("Peter", 25), ("Petra", 17), ("Bob", 40), ("Alice", 30)]:
        make_user(name, age)


def names(resp):
    assert resp.status_code == 200
    return [u["name"] for u in resp.json()["results"]]


def test_age_range(api_client, people):
    assert names(api_client.get(USERS_URL, {"min_age": 18, "max_age": 30})) == ["Peter", "Alice"]


def test_name_icontains(api_client, people):
    assert names(api_client.get(USERS_URL, {"name": "PET"})) == ["Peter", "Petra"]


def test_search(api_client, people):
    assert names(api_client.get(USERS_URL, {"search": "ali"})) == ["Alice"]


def test_ordering(api_client, people):
    assert names(api_client.get(USERS_URL, {"ordering": "-age"})) == ["Bob", "Alice", "Peter", "Petra"]


def test_invalid_filter_value_returns_400(api_client, people):
    assert api_client.get(USERS_URL, {"min_age": "old"}).status_code == 400


def test_default_page_size(api_client, make_user):
    for i in range(12):
        make_user(f"User{i}", 20)

    body = api_client.get(USERS_URL).json()

    assert body["count"] == 12
    assert len(body["results"]) == 10
    assert body["next"] is not None


def test_page_size_param(api_client, make_user):
    for i in range(12):
        make_user(f"User{i}", 20)

    body = api_client.get(USERS_URL, {"page": 2, "page_size": 5}).json()

    assert [u["name"] for u in body["results"]] == [f"User{i}" for i in range(5, 10)]


def test_page_size_is_capped(api_client, make_user):
    for i in range(105):
        make_user(f"User{i}", 20)

    body = api_client.get(USERS_URL, {"page_size": 1000}).json()

    assert len(body["results"]) == 100
