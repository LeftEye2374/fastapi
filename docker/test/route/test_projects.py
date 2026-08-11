import pytest


@pytest.mark.asyncio
async def test_create_project_success(client, auth_headers):
    response = await client.post("/projects/", json={"name": "P1"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "P1"


@pytest.mark.asyncio
async def test_create_project_unautorized(client):
    response = await client.post("/projects/", json={"name": "P1"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_project(client, auth_headers, other_user_headers):
    await client.post("/projects/", json={"name": "Mine"}, headers=auth_headers)
    await client.post(
        "/projects/",
        json={"name": "NotMine"},
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )

    response = await client.get("/projects/all", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    names = [p["name"] for p in body["items"]]
    assert names == ["Mine"]


@pytest.mark.asyncio
async def test_get_all_project_pagination(client, auth_headers):
    for i in range(3):
        await client.post("/projects/", json={"name": f"P{i}"}, headers=auth_headers)

    response = await client.get("/projects/all?limit=2&offset=1", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_get_my_project_by_id(client, auth_headers):
    create_resp = await client.post("/projects/", json={"name": "Mine"}, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == project_id


@pytest.mark.asyncio
async def test_get_other_project_by_id(client, auth_headers, other_user_headers):
    create_resp = await client.post("/projects/", json={"name": "Mine"}, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = await client.get(
        f"/projects/{project_id}",
        cookies=other_user_headers["cookies"],
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_project_with_wrong_id(client, auth_headers):
    response = await client.get("/projects/999999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_project_success(client, auth_headers):
    create_resp = await client.post("/projects/", json={"name": "Old"}, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = await client.put(
        f"/projects/{project_id}", json={"name": "New"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New"


@pytest.mark.asyncio
async def test_update_other_project(client, auth_headers, other_user_headers):
    create_resp = await client.post("/projects/", json={"name": "Mine"}, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = await client.put(
        f"/projects/{project_id}",
        json={"name": "Hacked"},
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_project_success(client, auth_headers):
    create_resp = await client.post("/projects/", json={"name": "ToDelete"}, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = await client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200

    check = await client.get(f"/projects/{project_id}", headers=auth_headers)
    assert check.status_code == 404


@pytest.mark.asyncio
async def test_delete_other_project(client, auth_headers, other_user_headers):
    create_resp = await client.post("/projects/", json={"name": "Mine"}, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = await client.delete(
        f"/projects/{project_id}",
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )
    assert response.status_code == 403
