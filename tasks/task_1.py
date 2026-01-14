#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from todolist import Task, TodoList


def main() -> None:
    todo_list: TodoList = TodoList()

    if os.path.exists("tasks.xml"):
        try:
            todo_list.load("tasks.xml")
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")

    print("Система управления списком задач (TODO)")
    print("Команды: add, list, select, sort, load, save, exit")
    print()

    while True:
        try:
            command: str = input("Введите команду: ").strip().lower()

            if command == "exit":
                print("До свидания!")
                break

            elif command == "add":
                text: str = input("Текст задачи: ").strip()
                priority: str = input("Приоритет (low/medium/high): ").strip().lower()
                status: str = (
                    input("Статус (new/in_progress/completed) [new]: ").strip().lower()
                    or "new"
                )

                todo_list.add(text, priority, status)
                todo_list.save("tasks.xml")
                print("Задача добавлена.\n")

            elif command == "list":
                print(todo_list)
                print()

            elif command == "select":
                filter_type: str = (
                    input("Выбрать по (status/priority): ").strip().lower()
                )

                if filter_type == "status":
                    select_status: str = (
                        input("Статус (new/in_progress/completed): ").strip().lower()
                    )
                    selected: list[Task] = todo_list.select_by_status(select_status)
                elif filter_type == "priority":
                    select_priority: str = (
                        input("Приоритет (low/medium/high): ").strip().lower()
                    )
                    selected = todo_list.select_by_priority(select_priority)
                else:
                    print("Неверный параметр.\n")
                    continue

                if selected:
                    print(f"\nНайдено задач: {len(selected)}\n")
                    for idx, task in enumerate(selected, 1):
                        status_str: str = str(task.status)
                        priority_str: str = str(task.priority)
                        print(f"{idx}. {task.text} " f"[{priority_str}, {status_str}]")
                else:
                    print("Задачи не найдены.")
                print()

            elif command == "sort":
                todo_list.sort_by_priority()
                todo_list.save("tasks.xml")
                print("Задачи отсортированы по приоритету.\n")
                print(todo_list)
                print()

            elif command == "load":
                load_filename: str = input("Имя XML файла: ").strip()
                todo_list.load(load_filename)
                print(f"Данные загружены из {load_filename}\n")

            elif command == "save":
                save_filename: str = input("Имя XML файла: ").strip()
                todo_list.save(save_filename)
                print(f"Данные сохранены в {save_filename}\n")

            else:
                print(
                    "Неизвестная команда. "
                    "Доступные команды: add, list, select, "
                    "sort, load, save, exit\n"
                )

        except ValueError as e:
            print(f"Ошибка: {e}\n")
        except Exception as e:
            print(f"Ошибка: {e}\n")


if __name__ == "__main__":
    main()
