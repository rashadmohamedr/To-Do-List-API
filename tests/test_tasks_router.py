"""Integration tests for task endpoints (/tasks/Tasks/)."""

import pytest


def _create_task(client, title, description=None):
    payload = {"title": title}
    if description is not None:
        payload["description"] = description
    return client.post("/tasks/Tasks/", json=payload)


class TestCreateTaskEndpoint:
    def test_create_task_returns_201_or_200(self, client):
        response = _create_task(client, "Buy groceries")
        assert response.status_code in (200, 201)

    def test_create_task_response_fields(self, client):
        response = _create_task(client, "Write tests", "Cover all endpoints")
        data = response.json()
        assert data["title"] == "Write tests"
        assert data["description"] == "Cover all endpoints"
        assert data["completed"] is False
        assert "id" in data

    def test_create_task_without_description(self, client):
        response = _create_task(client, "No description task")
        data = response.json()
        assert data["title"] == "No description task"
        assert data["description"] is None

    def test_create_task_missing_title_returns_422(self, client):
        response = client.post("/tasks/Tasks/", json={"description": "No title here"})
        assert response.status_code == 422


class TestListTasksEndpoint:
    def test_list_tasks_empty(self, client):
        response = client.get("/tasks/Tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_after_creation(self, client):
        _create_task(client, "Task One")
        _create_task(client, "Task Two")
        response = client.get("/tasks/Tasks/")
        assert response.status_code == 200
        titles = {t["title"] for t in response.json()}
        assert {"Task One", "Task Two"}.issubset(titles)

    def test_list_tasks_includes_all_fields(self, client):
        _create_task(client, "Detailed task", "Some detail")
        tasks = client.get("/tasks/Tasks/").json()
        task = next(t for t in tasks if t["title"] == "Detailed task")
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task


class TestToggleTaskEndpoint:
    def test_toggle_marks_task_completed(self, client):
        _create_task(client, "Toggle task")
        response = client.post("/tasks/Tasks/Toggle task/toggle")
        assert response.status_code == 200

    def test_toggle_nonexistent_task_returns_404(self, client):
        response = client.post("/tasks/Tasks/Ghost task/toggle")
        assert response.status_code == 404

    def test_toggle_reflects_in_list(self, client):
        _create_task(client, "Completable")
        client.post("/tasks/Tasks/Completable/toggle")
        tasks = client.get("/tasks/Tasks/").json()
        task = next(t for t in tasks if t["title"] == "Completable")
        assert task["completed"] is True

    def test_double_toggle_returns_to_incomplete(self, client):
        _create_task(client, "Reversible")
        client.post("/tasks/Tasks/Reversible/toggle")
        client.post("/tasks/Tasks/Reversible/toggle")
        tasks = client.get("/tasks/Tasks/").json()
        task = next(t for t in tasks if t["title"] == "Reversible")
        assert task["completed"] is False


class TestDeleteTaskEndpoint:
    def test_delete_existing_task(self, client):
        _create_task(client, "Delete me")
        response = client.delete("/tasks/Tasks/Delete me")
        assert response.status_code == 200

    def test_delete_removes_task_from_list(self, client):
        _create_task(client, "Gone soon")
        client.delete("/tasks/Tasks/Gone soon")
        tasks = client.get("/tasks/Tasks/").json()
        assert all(t["title"] != "Gone soon" for t in tasks)

    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.delete("/tasks/Tasks/Does not exist")
        assert response.status_code == 404

    def test_delete_only_removes_target(self, client):
        _create_task(client, "Keep me")
        _create_task(client, "Remove me")
        client.delete("/tasks/Tasks/Remove me")
        tasks = client.get("/tasks/Tasks/").json()
        titles = [t["title"] for t in tasks]
        assert "Keep me" in titles
        assert "Remove me" not in titles
