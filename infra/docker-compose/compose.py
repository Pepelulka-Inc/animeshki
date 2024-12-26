import argparse
import subprocess
import os.path

import prettytable

from attr import dataclass
from typing import List


@dataclass
class Service:
    short_name: str  # Имя используемое для идентификации сервиса в контексте этого питоновского скрипта
    compose_name: str  # Имя которое используется в файле compose.***.yml. compose_name - то что вместо звездочек
    depends_on: List[str]  # Список short_name'ов, от которых зависит этот сервис


# Список всех сервисов
SERVICES = [
    Service(short_name="postgres", compose_name="postgres", depends_on=[]),
    Service(short_name="auth", compose_name="auth-service", depends_on=["postgres"]),
    Service(short_name="main", compose_name="main-service", depends_on=["postgres"]),
    Service(short_name="nginx", compose_name="nginx", depends_on=["minio"]),
    Service(short_name="search", compose_name="search-service", depends_on=[]),
    Service(short_name="minio", compose_name="minio-service", depends_on=[]),
]

SERVICES_DICT = {service.short_name: service for service in SERVICES}

SERVICES_LIST = [service.short_name for service in SERVICES]


def command_list():
    table = prettytable.PrettyTable()
    table.field_names = [
        "Короткое имя",
        "Имя в названии докер компоуз файла",
        "Зависимости",
    ]
    for service in SERVICES:
        table.add_row(
            [service.short_name, service.compose_name, ", ".join(service.depends_on)]
        )
    print(table)

def resolve_deps(args):
    result = args.copy()
    for arg in args:
        for dep in SERVICES_DICT[arg].depends_on:
            if dep not in result:
                result.append(dep)
    return result

def compose_up(args, debug, detach):
    cmdline = ["docker-compose", "-f", "compose.yml"]
    for arg in args:
        cmdline += ["-f", f"services/compose.{SERVICES_DICT[arg].compose_name}.yml"]
        if debug:
            debug_compose_file_path = f"debug/compose.debug.{SERVICES_DICT[arg].compose_name}.yml"
            if not os.path.exists(debug_compose_file_path):
                continue
            cmdline += [
                "-f",
                debug_compose_file_path,
            ]
    cmdline.append("up")
    if detach:
        cmdline.append("-d")
    subprocess.call(cmdline)


def compose_down(args):
    cmdline = ["docker-compose", "-f", "compose.yml"]
    for arg in args:
        cmdline += ["-f", f"services/compose.{SERVICES_DICT[arg].compose_name}.yml"]
    cmdline.append("down")
    subprocess.call(cmdline)


def compose_build(args):
    cmdline = ["docker-compose", "-f", "compose.yml"]
    for arg in args:
        cmdline += ["-f", f"services/compose.{SERVICES_DICT[arg].compose_name}.yml"]
    cmdline.append("build")
    subprocess.call(cmdline)


def filter_args_inplace(args) -> bool:
    args = list(dict.fromkeys(args))

    # Очень костыльная и медленная реализация топологической сортировки
    result = []
    max_try_count = len(SERVICES) + 1
    try_count = 0
    while len(result) != len(args) and try_count <= max_try_count:
        try_count += 1
        for arg in args:
            if arg in result:
                continue
            flag = True
            for dependency in SERVICES_DICT[arg].depends_on:
                if dependency not in result:
                    flag = False
                    break
            if flag:
                result.append(arg)
    if try_count > max_try_count:
        return False
    args = result
    return True


def command_up(_args, debug=False, detach=False):
    # Проверяем что пользователь ввел верные названия сервисов
    for s_name in _args:
        if s_name not in SERVICES_DICT:
            print(f"Нет такого сервиса: {s_name}")
            return

    args = resolve_deps(_args)
    success = filter_args_inplace(args)
    if not success:
        print(
            f"Что-то накосячено с набором сервисов."
        )
        return
    compose_up(args, debug, detach)


def command_down_all():
    args = SERVICES_LIST
    assert filter_args_inplace(args)
    compose_down(args)


def command_build(_args):
    for s_name in _args:
        if s_name not in SERVICES_DICT:
            print(f"Нет такого сервиса: {s_name}")
            return
    args = resolve_deps(_args)
    success = filter_args_inplace(args)
    if not success:
        print(
            f"Что-то накосячено с набором сервисов."
        )
        return
    compose_build(args)


def main():
    parser = argparse.ArgumentParser(
        prog="compose.py",
        description="Мяу мяу мяу. Инструкция в README.md. Список доступных действий: list, up, up-all, down-all, build, build-all",
        epilog="",
    )
    parser.add_argument(
        "action",
        type=str,
    )
    parser.add_argument("args", nargs="*")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-D", "--detach", action="store_true")

    args = parser.parse_args()

    if args.action == "list":
        command_list()
    elif args.action == "up":
        command_up(args.args, args.debug, args.detach)
    elif args.action == "up-all":
        command_up(SERVICES_LIST, args.debug)
    elif args.action == "down-all":
        command_down_all()
    elif args.action == "build":
        command_build(args.args)
    elif args.action == "build-all":
        command_build(SERVICES_LIST)
    else:
        print(
            "Хз че ты от меня хочешь. Список доступных действий: list, up, up-all, down-all, build, build-all"
        )


if __name__ == "__main__":
    main()
