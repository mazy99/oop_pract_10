#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import click
from todolist import Task, TodoList


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--text", required=True, prompt="Текст задачи", help="Текст задачи")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    required=True,
    prompt="Приоритет (low/medium/high)",
    help="Приоритет",
)
@click.option(
    "--status",
    type=click.Choice(["new", "in_progress", "completed"]),
    default="new",
    help="Статус",
)
def add(text: str, priority: str, status: str) -> None:
    todo_list: TodoList = TodoList()
    if os.path.exists("tasks.xml"):
        try:
            todo_list.load("tasks.xml")
        except Exception as e:
            click.echo(f"Ошибка при загрузке: {e}", err=True)

    try:
        todo_list.add(text, priority, status)
        todo_list.save("tasks.xml")
        click.echo("✓ Задача добавлена.")
    except ValueError as e:
        click.echo(f"Ошибка: {e}", err=True)


@cli.command(name="list")
def list_tasks() -> None:
    todo_list: TodoList = TodoList()
    if os.path.exists("tasks.xml"):
        try:
            todo_list.load("tasks.xml")
        except Exception as e:
            click.echo(f"Ошибка при загрузке: {e}", err=True)
            return

    click.echo(todo_list)


@cli.command()
@click.option(
    "--status",
    type=click.Choice(["new", "in_progress", "completed"]),
    help="Фильтр по статусу",
)
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    help="Фильтр по приоритету",
)
def select(status: str | None, priority: str | None) -> None:
    if not status and not priority:
        click.echo("Укажите --status или --priority", err=True)
        return

    if status and priority:
        click.echo("Укажите только --status или только --priority", err=True)
        return

    todo_list: TodoList = TodoList()
    if os.path.exists("tasks.xml"):
        try:
            todo_list.load("tasks.xml")
        except Exception as e:
            click.echo(f"Ошибка при загрузке: {e}", err=True)
            return

    try:
        if status:
            selected: list[Task] = todo_list.select_by_status(status)
            filter_name: str = f"статусу '{status}'"
        else:
            selected = todo_list.select_by_priority(priority or "low")
            filter_name = f"приоритету '{priority}'"

        if selected:
            click.echo(f"Найдено задач по {filter_name}: {len(selected)}\n")
            for idx, task_item in enumerate(selected, 1):
                status_str: str = str(task_item.status)
                priority_str: str = str(task_item.priority)
                click.echo(
                    f"{idx}. {task_item.text} " f"[{priority_str}, {status_str}]"
                )
        else:
            click.echo(f"Задачи не найдены по {filter_name}.")
    except ValueError as e:
        click.echo(f"Ошибка: {e}", err=True)


@cli.command()
def sort() -> None:
    todo_list: TodoList = TodoList()
    if os.path.exists("tasks.xml"):
        try:
            todo_list.load("tasks.xml")
        except Exception as e:
            click.echo(f"Ошибка при загрузке: {e}", err=True)
            return

    try:
        todo_list.sort_by_priority()
        todo_list.save("tasks.xml")
        click.echo("✓ Задачи отсортированы по приоритету.")
        click.echo(todo_list)
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)


@cli.command()
@click.argument("filename")
def load(filename: str) -> None:
    todo_list: TodoList = TodoList()
    try:
        todo_list.load(filename)
        click.echo(f"✓ Данные загружены из {filename}")
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)


@cli.command()
@click.argument("filename")
def save(filename: str) -> None:
    todo_list: TodoList = TodoList()
    if os.path.exists("tasks.xml"):
        try:
            todo_list.load("tasks.xml")
        except Exception as e:
            click.echo(f"Ошибка при загрузке: {e}", err=True)
            return

    try:
        todo_list.save(filename)
        click.echo(f"✓ Данные сохранены в {filename}")
    except Exception as e:
        click.echo(f"Ошибка: {e}", err=True)


if __name__ == "__main__":
    cli()
