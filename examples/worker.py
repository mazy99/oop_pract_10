#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Worker:
    name: str
    post: str
    year: int


@dataclass
class Staff:
    workers: list[Worker] = field(default_factory=list)

    def add(self, name: str, post: str, year: int) -> None:
        self.workers.append(Worker(name=name, post=post, year=year))
        self.workers.sort(key=lambda worker: worker.name)

    def __str__(self) -> str:
        table: list[str] = []
        line: str = f"+-{'-' * 4}-+-{'-' * 30}-+-{'-' * 20}-+-{'-' * 8}-+"
        table.append(line)
        table.append(f"| {'№':^4} | {'Ф.И.О.':^30} | {'Должность':^20} | {'Год':^8} |")
        table.append(line)

        for idx, worker in enumerate(self.workers, 1):
            fmt_str: str = f"| {idx:>4} | {worker.name:<30} | "
            fmt_str += f"{worker.post:<20} | {worker.year:>8} |"
            table.append(fmt_str)

        table.append(line)
        return "\n".join(table)

    def select(self, period: int) -> list[Worker]:
        today: date = date.today()
        result: list[Worker] = []

        for worker in self.workers:
            if today.year - worker.year >= period:
                result.append(worker)

        return result

    def load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fin:
            xml: str = fin.read()

        parser: ET.XMLParser = ET.XMLParser(encoding="utf-8")
        tree: ET.Element = ET.fromstring(xml, parser=parser)

        self.workers = []
        for worker_element in tree:
            name: str | None = None
            post: str | None = None
            year: int | None = None

            for element in worker_element:
                if element.tag == "name":
                    name = element.text
                elif element.tag == "post":
                    post = element.text
                elif element.tag == "year":
                    if element.text is not None:
                        year = int(element.text)

            if name is not None and post is not None and year is not None:
                self.workers.append(Worker(name=name, post=post, year=year))

    def save(self, filename: str) -> None:
        root: ET.Element = ET.Element("workers")

        for worker in self.workers:
            worker_element: ET.Element = ET.Element("worker")

            name_element: ET.Element = ET.SubElement(worker_element, "name")
            name_element.text = worker.name

            post_element: ET.Element = ET.SubElement(worker_element, "post")
            post_element.text = worker.post

            year_element: ET.Element = ET.SubElement(worker_element, "year")
            year_element.text = str(worker.year)

            root.append(worker_element)

        tree: ET.ElementTree = ET.ElementTree(root)
        with open(filename, "wb") as fout:
            tree.write(fout, encoding="utf-8", xml_declaration=True)


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Система учёта сотрудников (dataclass + XML + argparse)"
    )

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest="command")

    add_parser: argparse.ArgumentParser = subparsers.add_parser(
        "add", help="Добавить сотрудника"
    )
    add_parser.add_argument("--name", required=True, help="Фамилия и инициалы")
    add_parser.add_argument("--post", required=True, help="Должность")
    add_parser.add_argument("--year", required=True, type=int, help="Год поступления")

    subparsers.add_parser("list", help="Показать всех сотрудников")

    select_parser: argparse.ArgumentParser = subparsers.add_parser(
        "select", help="Выбрать по стажу"
    )
    select_parser.add_argument("--period", required=True, type=int, help="Стаж (годы)")

    load_parser: argparse.ArgumentParser = subparsers.add_parser(
        "load", help="Загрузить из XML"
    )
    load_parser.add_argument("filename", help="Имя XML файла")

    save_parser: argparse.ArgumentParser = subparsers.add_parser(
        "save", help="Сохранить в XML"
    )
    save_parser.add_argument("filename", help="Имя XML файла")

    return parser


def main() -> None:
    staff: Staff = Staff()

    import os

    if os.path.exists("staff.xml"):
        staff.load("staff.xml")

    print("Система учёта сотрудников")
    print("Команды: add, list, select, load, save, exit")
    print()

    while True:
        try:
            command: str = input("Введите команду: ").strip()

            if command == "exit":
                print("До свидания!")
                break

            elif command == "add":
                name: str = input("Фамилия и инициалы: ").strip()
                post: str = input("Должность: ").strip()
                year: int = int(input("Год поступления: ").strip())
                staff.add(name, post, year)
                staff.save("staff.xml")
                print("✓ Сотрудник добавлен.")

            elif command == "list":
                print(staff)

            elif command == "select":
                period: int = int(input("Стаж (годы): ").strip())
                selected: list[Worker] = staff.select(period)
                if selected:
                    print(f"\nСотрудники со стажем >= {period} лет:")
                    for idx, worker in enumerate(selected, 1):
                        print(
                            f"{idx:>4}: {worker.name} - {worker.post} ({worker.year})"
                        )
                else:
                    print("Работники с заданным стажем не найдены.")

            elif command == "load":
                load_filename: str = input("Имя XML файла: ").strip()
                staff.load(load_filename)
                print(f"✓ Данные загружены из {load_filename}")

            elif command == "save":
                filename: str = input("Имя XML файла: ").strip()
                staff.save(filename)
                print(f"✓ Данные сохранены в {filename}")

            else:
                msg: str = "Неизвестная команда. Доступные команды: "
                msg += "add, list, select, load, save, exit"
                print(msg)

            print()

        except ValueError:
            print("Ошибка: неверное значение. Попробуйте снова.")
            print()
        except Exception as e:
            print(f"Ошибка: {e}")
            print()


if __name__ == "__main__":
    main()
