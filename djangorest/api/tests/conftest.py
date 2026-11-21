import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from api.models import User

USERS_URL = "/api/users/"
TOKEN_URL = "/api/auth/token/"
PASSWORD = "s3cret-pass-123"


def detail_url(pk):
    return f"{USERS_URL}{pk}/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def account(db):
    """A Django auth account that can log in (not the api.User resource)."""
    return get_user_model().objects.create_user(username="admin", password=PASSWORD)


@pytest.fixture
def tokens(api_client, account):
    resp = api_client.post(TOKEN_URL, {"username": "admin", "password": PASSWORD}, format="json")
    assert resp.status_code == 200
    return resp.json()


@pytest.fixture
def auth_client(tokens):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    return client


@pytest.fixture
def make_user(db):
    def _make(name="Peter", age=25):
        return User.objects.create(name=name, age=age)

    return _make
