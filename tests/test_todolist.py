#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile

import pytest
from todolist import Priority, Status, Task, TodoList


class TestPriority:
    def test_priority_values(self):
        assert Priority.LOW.value == 1
        assert Priority.MEDIUM.value == 2
        assert Priority.HIGH.value == 3

    def test_priority_str(self):
        assert str(Priority.LOW) == "LOW"
        assert str(Priority.MEDIUM) == "MEDIUM"
        assert str(Priority.HIGH) == "HIGH"


class TestStatus:
    def test_status_values(self):
        assert Status.NEW.value == "новая"
        assert Status.IN_PROGRESS.value == "в работе"
        assert Status.COMPLETED.value == "выполнена"

    def test_status_str(self):
        assert str(Status.NEW) == "новая"
        assert str(Status.IN_PROGRESS) == "в работе"
        assert str(Status.COMPLETED) == "выполнена"


class TestTask:
    def test_task_creation(self):
        task = Task(text="Test task", priority=Priority.HIGH, status=Status.NEW)
        assert task.text == "Test task"
        assert task.priority == Priority.HIGH
        assert task.status == Status.NEW

    def test_task_is_frozen(self):
        task = Task(text="Test task", priority=Priority.LOW, status=Status.NEW)
        with pytest.raises(AttributeError):
            task.text = "Changed"


class TestTodoList:
    def test_empty_creation(self):
        todo_list = TodoList()
        assert len(todo_list.tasks) == 0

    def test_add_task(self):
        todo_list = TodoList()
        todo_list.add("Test task", "high", "new")
        assert len(todo_list.tasks) == 1
        assert todo_list.tasks[0].text == "Test task"

    def test_add_multiple_tasks(self):
        todo_list = TodoList()
        todo_list.add("Task 1", "high", "new")
        todo_list.add("Task 2", "low", "completed")
        assert len(todo_list.tasks) == 2

    def test_add_case_insensitive(self):
        todo_list = TodoList()
        todo_list.add("Task 1", "Low", "NEW")
        todo_list.add("Task 2", "MEDIUM", "in_progress")
        assert todo_list.tasks[0].priority == Priority.LOW
        assert todo_list.tasks[1].priority == Priority.MEDIUM

    def test_add_invalid_priority(self):
        todo_list = TodoList()
        with pytest.raises(ValueError):
            todo_list.add("Task", "invalid", "new")

    def test_add_invalid_status(self):
        todo_list = TodoList()
        with pytest.raises(ValueError):
            todo_list.add("Task", "low", "invalid")

    def test_select_by_status(self):
        todo_list = TodoList()
        todo_list.add("Task 1", "high", "new")
        todo_list.add("Task 2", "low", "new")
        todo_list.add("Task 3", "medium", "completed")

        new_tasks = todo_list.select_by_status("new")
        assert len(new_tasks) == 2
        assert all(task.status == Status.NEW for task in new_tasks)

    def test_select_by_status_empty(self):
        todo_list = TodoList()
        todo_list.add("Task", "low", "new")
        completed = todo_list.select_by_status("completed")
        assert len(completed) == 0

    def test_select_by_status_invalid(self):
        todo_list = TodoList()
        with pytest.raises(ValueError):
            todo_list.select_by_status("invalid")

    def test_select_by_priority(self):
        todo_list = TodoList()
        todo_list.add("Task 1", "high", "new")
        todo_list.add("Task 2", "high", "completed")
        todo_list.add("Task 3", "low", "new")

        high_tasks = todo_list.select_by_priority("high")
        assert len(high_tasks) == 2
        assert all(task.priority == Priority.HIGH for task in high_tasks)

    def test_select_by_priority_empty(self):
        todo_list = TodoList()
        todo_list.add("Task", "low", "new")
        high = todo_list.select_by_priority("high")
        assert len(high) == 0

    def test_select_by_priority_invalid(self):
        todo_list = TodoList()
        with pytest.raises(ValueError):
            todo_list.select_by_priority("invalid")

    def test_sort_by_priority(self):
        todo_list = TodoList()
        todo_list.add("Task 1", "low", "new")
        todo_list.add("Task 2", "high", "new")
        todo_list.add("Task 3", "medium", "new")

        todo_list.sort_by_priority()

        assert todo_list.tasks[0].priority == Priority.HIGH
        assert todo_list.tasks[1].priority == Priority.MEDIUM
        assert todo_list.tasks[2].priority == Priority.LOW

    def test_str_representation(self):
        todo_list = TodoList()
        todo_list.add("Test task", "high", "new")

        str_repr = str(todo_list)
        assert "Test task" in str_repr
        assert "HIGH" in str_repr
        assert "новая" in str_repr

    def test_str_empty_list(self):
        todo_list = TodoList()
        assert str(todo_list) == "Список задач пуст."

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "tasks.xml")

            todo_list1 = TodoList()
            todo_list1.add("Task 1", "high", "new")
            todo_list1.add("Task 2", "low", "completed")
            todo_list1.save(filename)

            todo_list2 = TodoList()
            todo_list2.load(filename)

            assert len(todo_list2.tasks) == 2
            assert todo_list2.tasks[0].text == "Task 1"
            assert todo_list2.tasks[1].status == Status.COMPLETED

    def test_save_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "test.xml")
            todo_list = TodoList()
            todo_list.add("Task", "medium", "new")
            todo_list.save(filename)

            assert os.path.exists(filename)
            assert os.path.getsize(filename) > 0

    def test_load_nonexistent_file(self):
        todo_list = TodoList()
        with pytest.raises(FileNotFoundError):
            todo_list.load("nonexistent.xml")

    def test_workflow(self):
        todo_list = TodoList()
        todo_list.add("Write report", "high", "new")
        todo_list.add("Review code", "high", "in_progress")
        todo_list.add("Test features", "medium", "new")
        todo_list.add("Documentation", "low", "new")

        high_priority = todo_list.select_by_priority("high")
        assert len(high_priority) == 2

        new_tasks = todo_list.select_by_status("new")
        assert len(new_tasks) == 3

        todo_list.sort_by_priority()
        assert todo_list.tasks[0].priority == Priority.HIGH
        assert todo_list.tasks[-1].priority == Priority.LOW

        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "tasks.xml")
            todo_list.save(filename)

            new_list = TodoList()
            new_list.load(filename)
            assert len(new_list.tasks) == 4
