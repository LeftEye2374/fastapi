import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def project_with_task(client, auth_headers):
    """Проект + одна задача в нём, оба принадлежат пользователю из auth_headers."""
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
async def test_create_task_success(client, auth_headers):
    project_resp = await client.post("/projects/", json={"name": "P"}, headers=auth_headers)
    project_id = project_resp.json()["id"]

    response = await client.post(
        f"/tasks/?project_id={project_id}",
        json={
            "title": "title",
            "description": "description",
            "deadline": "2026-01-01",
            "status": "todo",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["project_id"] == project_id


@pytest.mark.asyncio
async def test_create_task_with_explicit_assignee(client, auth_headers, other_user_headers):
    project_resp = await client.post("/projects/", json={"name": "P"}, headers=auth_headers)
    project_id = project_resp.json()["id"]

    me_resp = await client.get("/auth/me", cookies=other_user_headers["cookies"])
    other_user_id = me_resp.json()["id"]

    response = await client.post(
        f"/tasks/?project_id={project_id}",
        json={
            "title": "T",
            "description": "d",
            "deadline": "2026-01-01",
            "status": "todo",
            "assignee_id": other_user_id,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["assignee_id"] == other_user_id


@pytest.mark.asyncio
async def test_create_task_unauthorized(client):
    response = await client.post(
        "/tasks/?project_id=1",
        json={"title": "T", "description": "d", "deadline": "2026-01-01", "status": "todo"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_tasks_of_project(client, auth_headers, project_with_task):
    project_id, task_id = project_with_task

    response = await client.get(f"/tasks/all?project_id={project_id}", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    ids = [t["id"] for t in body["items"]]
    assert ids == [task_id]


@pytest.mark.asyncio
async def test_get_all_tasks_filter_by_status(client, auth_headers, project_with_task):
    project_id, task_id = project_with_task
    await client.put(
        f"/tasks/{task_id}",
        json={"title": "T", "description": "d", "deadline": "2026-01-01", "status": "done"},
        headers=auth_headers,
    )
    await client.post(
        f"/tasks/?project_id={project_id}",
        json={"title": "T2", "description": "d", "deadline": "2026-01-01", "status": "todo"},
        headers=auth_headers,
    )

    response = await client.get(
        f"/tasks/all?project_id={project_id}&status=done", headers=auth_headers
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == task_id


@pytest.mark.asyncio
async def test_get_all_tasks_of_other_project(client, other_user_headers, project_with_task):
    project_id, _ = project_with_task

    response = await client.get(
        f"/tasks/all?project_id={project_id}",
        cookies=other_user_headers["cookies"],
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_tasks_of_nonexistent_project(client, auth_headers):
    response = await client.get("/tasks/all?project_id=999999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_task_by_id_success(client, auth_headers, project_with_task):
    _, task_id = project_with_task

    response = await client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_by_id_other_project(client, other_user_headers, project_with_task):
    _, task_id = project_with_task

    response = await client.get(f"/tasks/{task_id}", cookies=other_user_headers["cookies"])
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_task_with_wrong_id(client, auth_headers):
    response = await client.get("/tasks/999999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_success(client, auth_headers, project_with_task):
    _, task_id = project_with_task

    response = await client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated",
            "description": "d2",
            "deadline": "2026-02-02",
            "status": "in_progress",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_update_task_reassign(client, auth_headers, other_user_headers, project_with_task):
    _, task_id = project_with_task

    me_resp = await client.get("/auth/me", cookies=other_user_headers["cookies"])
    other_user_id = me_resp.json()["id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={
            "title": "T",
            "description": "d",
            "deadline": "2026-01-01",
            "status": "todo",
            "assignee_id": other_user_id,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["assignee_id"] == other_user_id


@pytest.mark.asyncio
async def test_update_other_project_task(client, other_user_headers, project_with_task):
    _, task_id = project_with_task

    response = await client.put(
        f"/tasks/{task_id}",
        json={"title": "Hacked", "description": "d", "deadline": "2026-01-01", "status": "todo"},
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_task_success(client, auth_headers, project_with_task):
    _, task_id = project_with_task

    response = await client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200

    check = await client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert check.status_code == 404


@pytest.mark.asyncio
async def test_delete_other_project_task(client, other_user_headers, project_with_task):
    _, task_id = project_with_task

    response = await client.delete(
        f"/tasks/{task_id}",
        cookies=other_user_headers["cookies"],
        headers=other_user_headers["headers"],
    )
    assert response.status_code == 403
