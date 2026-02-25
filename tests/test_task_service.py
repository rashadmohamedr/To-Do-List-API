"""Unit tests for task service functions in app/services/task_service.py."""

import pytest
from fastapi import HTTPException

from app.schemas.task import TaskCreate
from app.services.task_service import create_task, list_tasks, toggle_task, delete_task


class TestCreateTask:
    def test_creates_task_with_title(self, db):
        task = create_task(TaskCreate(title="Buy milk"), db)
        assert task.id is not None
        assert task.title == "Buy milk"
        assert task.completed is False

    def test_creates_task_with_description(self, db):
        task = create_task(TaskCreate(title="Read book", description="Read chapter 1"), db)
        assert task.description == "Read chapter 1"

    def test_creates_task_without_description(self, db):
        task = create_task(TaskCreate(title="No desc"), db)
        assert task.description is None

    def test_task_is_persisted(self, db):
        create_task(TaskCreate(title="Persistent task"), db)
        tasks = list_tasks(db)
        titles = [t.title for t in tasks]
        assert "Persistent task" in titles


class TestListTasks:
    def test_returns_empty_list_initially(self, db):
        tasks = list_tasks(db)
        assert tasks == []

    def test_returns_all_created_tasks(self, db):
        create_task(TaskCreate(title="Task A"), db)
        create_task(TaskCreate(title="Task B"), db)
        tasks = list_tasks(db)
        assert len(tasks) == 2

    def test_list_contains_correct_titles(self, db):
        create_task(TaskCreate(title="Alpha"), db)
        create_task(TaskCreate(title="Beta"), db)
        titles = {t.title for t in list_tasks(db)}
        assert titles == {"Alpha", "Beta"}


class TestToggleTask:
    def test_toggle_marks_task_completed(self, db):
        create_task(TaskCreate(title="Toggle me"), db)
        toggle_task("Toggle me", db)
        tasks = list_tasks(db)
        task = next(t for t in tasks if t.title == "Toggle me")
        assert task.completed is True

    def test_toggle_twice_returns_to_incomplete(self, db):
        create_task(TaskCreate(title="Flip flop"), db)
        toggle_task("Flip flop", db)
        toggle_task("Flip flop", db)
        tasks = list_tasks(db)
        task = next(t for t in tasks if t.title == "Flip flop")
        assert task.completed is False

    def test_toggle_nonexistent_task_raises_404(self, db):
        with pytest.raises(HTTPException) as exc_info:
            toggle_task("Ghost task", db)
        assert exc_info.value.status_code == 404


class TestDeleteTask:
    def test_delete_existing_task(self, db):
        create_task(TaskCreate(title="Delete me"), db)
        response = delete_task("Delete me", db)
        assert response.status_code == 200
        assert list_tasks(db) == []

    def test_delete_nonexistent_task_returns_404(self, db):
        response = delete_task("Nonexistent", db)
        assert response.status_code == 404

    def test_delete_only_removes_target_task(self, db):
        create_task(TaskCreate(title="Keep me"), db)
        create_task(TaskCreate(title="Remove me"), db)
        delete_task("Remove me", db)
        remaining = [t.title for t in list_tasks(db)]
        assert remaining == ["Keep me"]
        assert "Remove me" not in remaining
