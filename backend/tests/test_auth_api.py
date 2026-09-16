from tests.db_support import auth_header, requires_postgres


@requires_postgres
def test_register_login_me_and_logout(api_client) -> None:
    register = api_client.post(
        "/api/v1/auth/register",
        json={"email": "owner@example.com", "password": "password12"},
    )
    assert register.status_code == 201, register.text
    token = register.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    me = api_client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "owner@example.com"

    login = api_client.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "password12"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == "owner@example.com"

    logout = api_client.post("/api/v1/auth/logout", headers=headers)
    assert logout.status_code == 204


@requires_postgres
def test_register_rejects_duplicate_and_short_password(api_client) -> None:
    first = api_client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "password12"},
    )
    assert first.status_code == 201
    duplicate = api_client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "password12"},
    )
    assert duplicate.status_code == 409
    short = api_client.post(
        "/api/v1/auth/register",
        json={"email": "short@example.com", "password": "short"},
    )
    assert short.status_code == 422


@requires_postgres
def test_me_requires_authentication(api_client) -> None:
    response = api_client.get("/api/v1/auth/me")
    assert response.status_code == 401


@requires_postgres
def test_profile_email_update(api_client) -> None:
    headers = auth_header(api_client, "profile@example.com")
    updated = api_client.patch(
        "/api/v1/auth/me",
        headers=headers,
        json={"email": "renamed@example.com"},
    )
    assert updated.status_code == 200
    assert updated.json()["email"] == "renamed@example.com"
