import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def project_with_task(client, auth_headers):
    project_resp = await client.post("/projects/", json={"name": "P"}, headers=auth_headers)
    project_id = project_resp.json()["id"]

    task_resp = await client.post(
        f"/tasks/?project_id={project_id}",
        json={"title": "T", "description": "d", "deadline": "2026-01-01", "status": "todo"},
        headers=auth_headers,
    )
    task_id = task_resp.json()["id"]
    return project_id, task_id


@pytest.mark.asyncio
async def test_create_tag_success(client, auth_headers):
    response = await client.post("/tags/", json={"name": "urgent"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "urgent"


@pytest.mark.asyncio
async def test_get_all_tags(client, auth_headers):
    await client.post("/tags/", json={"name": "urgent"}, headers=auth_headers)
    await client.post("/tags/", json={"name": "bug"}, headers=auth_headers)

    response = await client.get("/tags/", headers=auth_headers)
    assert response.status_code == 200
    names = {t["name"] for t in response.json()}
    assert names == {"urgent", "bug"}


@pytest.mark.asyncio
async def test_add_tag_to_task_success(client, auth_headers, project_with_task):
    _, task_id = project_with_task
    tag_resp = await client.post("/tags/", json={"name": "urgent"}, headers=auth_headers)
    tag_id = tag_resp.json()["id"]

    response = await client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)
    assert response.status_code == 200

    task_resp = await client.get(f"/tasks/{task_id}", headers=auth_headers)
    tag_names = [t["name"] for t in task_resp.json()["tags"]]
    assert tag_names == ["urgent"]


@pytest.mark.asyncio
async def test_add_tag_to_other_project_task(client, auth_headers, other_user_headers, project_with_task):
    _, task_id = project_with_task
    tag_resp = await client.post("/tags/", json={"name": "urgent"}, headers=auth_headers)
    tag_id = tag_resp.json()["id"]

    response = await client.post(
        f"/tasks/{task_id}/tags/{tag_id}",
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_remove_tag_from_task_success(client, auth_headers, project_with_task):
    _, task_id = project_with_task
    tag_resp = await client.post("/tags/", json={"name": "urgent"}, headers=auth_headers)
    tag_id = tag_resp.json()["id"]
    await client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)

    response = await client.delete(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)
    assert response.status_code == 200

    task_resp = await client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert task_resp.json()["tags"] == []


@pytest.mark.asyncio
async def test_remove_tag_from_other_project_task(client, auth_headers, other_user_headers, project_with_task):
    _, task_id = project_with_task
    tag_resp = await client.post("/tags/", json={"name": "urgent"}, headers=auth_headers)
    tag_id = tag_resp.json()["id"]
    await client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)

    response = await client.delete(
        f"/tasks/{task_id}/tags/{tag_id}",
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )
    assert response.status_code == 403
