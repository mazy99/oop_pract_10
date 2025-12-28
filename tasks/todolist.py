#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __str__(self) -> str:
        return self.name


class Status(Enum):
    NEW = "новая"
    IN_PROGRESS = "в работе"
    COMPLETED = "выполнена"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Task:
    text: str
    priority: Priority
    status: Status


@dataclass
class TodoList:
    tasks: list[Task] = field(default_factory=list)

    def add(self, text: str, priority: str, status: str = "новая") -> None:
        try:
            pri: Priority = Priority[priority.upper()]
        except KeyError:
            raise ValueError(f"Invalid priority: {priority}")

        try:
            st: Status = Status[status.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Invalid status: {status}")

        self.tasks.append(Task(text=text, priority=pri, status=st))

    def __str__(self) -> str:
        if not self.tasks:
            return "Список задач пуст."

        table: list[str] = []
        line: str = f"+-{'-' * 3}-+-{'-' * 40}-+-{'-' * 10}-+-{'-' * 12}-+"
        table.append(line)
        table.append(
            f"| {'\u2116':^3} | {'\u0422\u0435\u043a\u0441\u0442':^40} | "
            f"{'\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442':^10} | "
            f"{'\u0421\u0442\u0430\u0442\u0443\u0441':^12} |"
        )
        table.append(line)

        for idx, task in enumerate(self.tasks, 1):
            fmt_str: str = f"| {idx:>3} | {task.text:<40} | "
            fmt_str += f"{str(task.priority):<10} | {str(task.status):<12} |"
            table.append(fmt_str)

        table.append(line)
        return "\n".join(table)

    def select_by_status(self, status: str) -> list[Task]:
        try:
            st: Status = Status[status.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Invalid status: {status}")

        return [task for task in self.tasks if task.status == st]

    def select_by_priority(self, priority: str) -> list[Task]:
        """Select tasks by priority."""
        try:
            pri: Priority = Priority[priority.upper()]
        except KeyError:
            raise ValueError(f"Invalid priority: {priority}")

        return [task for task in self.tasks if task.priority == pri]

    def sort_by_priority(self) -> None:
        self.tasks.sort(key=lambda task: task.priority.value, reverse=True)

    def load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fin:
            xml: str = fin.read()

        parser: ET.XMLParser = ET.XMLParser(encoding="utf-8")
        tree: ET.Element = ET.fromstring(xml, parser=parser)

        self.tasks = []
        for task_element in tree:
            text: str | None = None
            priority: str | None = None
            status: str | None = None

            for element in task_element:
                if element.tag == "text":
                    text = element.text
                elif element.tag == "priority":
                    priority = element.text
                elif element.tag == "status":
                    status = element.text

            if text and priority and status:
                self.add(text, priority, status)

    def save(self, filename: str) -> None:
        root: ET.Element = ET.Element("tasks")

        for task in self.tasks:
            task_element: ET.Element = ET.Element("task")

            text_element: ET.Element = ET.SubElement(task_element, "text")
            text_element.text = task.text

            priority_element: ET.Element = ET.SubElement(task_element, "priority")
            priority_element.text = task.priority.name

            status_element: ET.Element = ET.SubElement(task_element, "status")
            status_element.text = task.status.name

            root.append(task_element)

        tree: ET.ElementTree = ET.ElementTree(root)
        with open(filename, "wb") as fout:
            tree.write(fout, encoding="utf-8", xml_declaration=True)


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Система управления списком задач (dataclass + XML + argparse)"
    )

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest="command")

    add_parser: argparse.ArgumentParser = subparsers.add_parser(
        "add", help="Добавить задачу"
    )
    add_parser.add_argument("--text", required=True, help="Текст задачи")
    add_parser.add_argument(
        "--priority",
        required=True,
        choices=["low", "medium", "high"],
        help="Приоритет (low, medium, high)",
    )
    add_parser.add_argument(
        "--status",
        default="new",
        choices=["new", "in_progress", "completed"],
        help="Статус (new, in_progress, completed)",
    )

    subparsers.add_parser("list", help="Показать все задачи")

    select_parser: argparse.ArgumentParser = subparsers.add_parser(
        "select", help="Выбрать задачи"
    )
    select_group = select_parser.add_mutually_exclusive_group(required=True)
    select_group.add_argument(
        "--status",
        choices=["new", "in_progress", "completed"],
        help="Фильтр по статусу",
    )
    select_group.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        help="Фильтр по приоритету",
    )

    subparsers.add_parser("sort", help="Отсортировать по приоритету")

    load_parser: argparse.ArgumentParser = subparsers.add_parser(
        "load", help="Загрузить из XML"
    )
    load_parser.add_argument("filename", help="Имя XML файла")

    save_parser: argparse.ArgumentParser = subparsers.add_parser(
        "save", help="Сохранить в XML"
    )
    save_parser.add_argument("filename", help="Имя XML файла")

    return parser
