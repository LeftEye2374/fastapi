import pytest


@pytest.mark.asyncio
async def test_create_task_success():
    ...

@pytest.mark.asyncio
async def test_create_task_with_explicit_assignee():
    ...

@pytest.mark.asyncio
async def test_create_task_unauthorized():
    ...

@pytest.mark.asyncio
async def test_get_all_tasks_of_project():
    ...

@pytest.mark.asyncio
async def test_get_all_tasks_of_other_project():
    ...

@pytest.mark.asyncio
async def test_get_all_tasks_of_nonexistent_project():
    ...

@pytest.mark.asyncio
async def test_get_task_by_id_success():
    ...

@pytest.mark.asyncio
async def test_get_task_by_id_other_project():
    ...

@pytest.mark.asyncio
async def test_get_task_with_wrong_id():
    ...

@pytest.mark.asyncio
async def test_update_task_success():
    ...

@pytest.mark.asyncio
async def test_update_task_reassign():
    ...

@pytest.mark.asyncio
async def test_update_other_project_task():
    ...

@pytest.mark.asyncio
async def test_delete_task_success():
    ...

@pytest.mark.asyncio
async def test_delete_other_project_task():
    ...