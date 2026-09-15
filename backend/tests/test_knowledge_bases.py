from tests.db_support import auth_header, requires_postgres


@requires_postgres
def test_knowledge_base_crud_for_owner(api_client) -> None:
    headers = auth_header(api_client, "kb-owner@example.com")
    created = api_client.post(
        "/api/v1/knowledge-bases",
        headers=headers,
        json={"name": "Handbook", "description": "HR policies"},
    )
    assert created.status_code == 201, created.text
    kb_id = created.json()["id"]

    listed = api_client.get("/api/v1/knowledge-bases", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = api_client.get(f"/api/v1/knowledge-bases/{kb_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Handbook"

    patched = api_client.patch(
        f"/api/v1/knowledge-bases/{kb_id}",
        headers=headers,
        json={"name": "Employee Handbook"},
    )
    assert patched.status_code == 200
    assert patched.json()["name"] == "Employee Handbook"

    deleted = api_client.delete(f"/api/v1/knowledge-bases/{kb_id}", headers=headers)
    assert deleted.status_code == 204
    missing = api_client.get(f"/api/v1/knowledge-bases/{kb_id}", headers=headers)
    assert missing.status_code == 404


@requires_postgres
def test_user_cannot_access_another_users_knowledge_base(api_client) -> None:
    owner_headers = auth_header(api_client, "owner@example.com")
    stranger_headers = auth_header(api_client, "stranger@example.com")
    created = api_client.post(
        "/api/v1/knowledge-bases",
        headers=owner_headers,
        json={"name": "Private KB"},
    )
    kb_id = created.json()["id"]

    listed = api_client.get("/api/v1/knowledge-bases", headers=stranger_headers)
    assert listed.status_code == 200
    assert listed.json() == []

    fetched = api_client.get(f"/api/v1/knowledge-bases/{kb_id}", headers=stranger_headers)
    assert fetched.status_code == 404

    patched = api_client.patch(
        f"/api/v1/knowledge-bases/{kb_id}",
        headers=stranger_headers,
        json={"name": "Hijacked"},
    )
    assert patched.status_code == 404

    deleted = api_client.delete(f"/api/v1/knowledge-bases/{kb_id}", headers=stranger_headers)
    assert deleted.status_code == 404

    still_there = api_client.get(f"/api/v1/knowledge-bases/{kb_id}", headers=owner_headers)
    assert still_there.status_code == 200
    assert still_there.json()["name"] == "Private KB"


@requires_postgres
def test_knowledge_bases_require_auth(api_client) -> None:
    response = api_client.get("/api/v1/knowledge-bases")
    assert response.status_code == 401
