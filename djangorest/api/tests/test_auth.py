import pytest

from .conftest import PASSWORD, TOKEN_URL, USERS_URL, detail_url

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "method, use_detail",
    [("post", False), ("put", True), ("patch", True), ("delete", True)],
)
def test_writes_require_auth(api_client, make_user, method, use_detail):
    user = make_user()
    url = detail_url(user.pk) if use_detail else USERS_URL

    resp = getattr(api_client, method)(url, {"name": "Bob", "age": 30}, format="json")

    assert resp.status_code == 401


def test_wrong_password_rejected(api_client, account):
    resp = api_client.post(TOKEN_URL, {"username": "admin", "password": "wrong"}, format="json")

    assert resp.status_code == 401


def test_token_pair_issued(tokens):
    assert {"access", "refresh"} <= tokens.keys()


def test_refresh_returns_new_access_token(api_client, tokens):
    resp = api_client.post(f"{TOKEN_URL}refresh/", {"refresh": tokens["refresh"]}, format="json")

    assert resp.status_code == 200
    assert "access" in resp.json()


def test_verify(api_client, tokens):
    ok = api_client.post(f"{TOKEN_URL}verify/", {"token": tokens["access"]}, format="json")
    bad = api_client.post(f"{TOKEN_URL}verify/", {"token": "not-a-token"}, format="json")

    assert ok.status_code == 200
    assert bad.status_code == 401


def test_bogus_bearer_token_rejected(api_client):
    api_client.credentials(HTTP_AUTHORIZATION="Bearer garbage")

    resp = api_client.post(USERS_URL, {"name": "Bob", "age": 30}, format="json")

    assert resp.status_code == 401


def test_session_login_also_works(api_client, account):
    assert api_client.login(username="admin", password=PASSWORD)

    resp = api_client.post(USERS_URL, {"name": "Bob", "age": 30}, format="json")

    assert resp.status_code == 201
