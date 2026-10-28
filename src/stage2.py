"""Эмулятор командной строки. Вариант 3. Этап 2: конфигурация.

Параметры командной строки: путь к VFS, пользовательское приглашение,
путь к стартовому скрипту. При запуске выводятся все параметры
(отладочный вывод), служебная команда conf-dump печатает их в формате
ключ-значение. Стартовый скрипт выполняется с отображением ввода и
вывода и останавливается при первой ошибке.
"""

import argparse
import sys

from src.stage1 import EXIT_ERROR, Emulator1


class Emulator2(Emulator1):
    """Эмулятор с параметрами командной строки и стартовым скриптом."""

    def __init__(self, vfs_path=None, custom_prompt=None,
                 script_path=None):
        """Сохранить параметры, заданные пользователем."""
        super().__init__()
        self.vfs_path = vfs_path
        self.custom_prompt = custom_prompt
        self.script_path = script_path

    def get_prompt(self):
        """Пользовательское приглашение или стандартное."""
        if self.custom_prompt:
            return self.custom_prompt
        return super().get_prompt()

    def config_items(self):
        """Параметры эмулятора в виде списка пар (ключ, значение)."""
        return [
            ("vfs_path", self.vfs_path),
            ("custom_prompt", self.custom_prompt),
            ("script_path", self.script_path),
        ]

    def get_commands(self):
        """Добавить служебную команду conf-dump."""
        commands = super().get_commands()
        commands["conf-dump"] = self.cmd_conf_dump
        return commands

    def cmd_conf_dump(self, args):
        """Вывести параметры эмулятора в формате ключ-значение."""
        if args:
            print("conf-dump: too many arguments")
            return False
        for key, value in self.config_items():
            print(f"{key}={value}")
        return True

    def print_config(self):
        """Отладочный вывод всех параметров при запуске."""
        print("--- emulator configuration ---")
        for key, value in self.config_items():
            print(f"{key}={value}")
        print("------------------------------")

    def run_script(self):
        """Выполнить стартовый скрипт. Возвращает True при успехе.

        Каждая команда выводится вместе с приглашением, как при вводе
        пользователем. Пустые строки и строки, начинающиеся с #,
        пропускаются. Выполнение останавливается при первой ошибке.
        """
        try:
            with open(self.script_path, encoding="utf-8") as handle:
                lines = handle.readlines()
        except OSError as error:
            print(f"script error: cannot read '{self.script_path}': "
                  f"{error.strerror}")
            return False
        for number, raw in enumerate(lines, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{self.get_prompt()}{line}")
            if not self.handle_line(line):
                print(f"script error: execution stopped at line {number}")
                return False
            if not self.running:
                break
        return True

    def run(self):
        """Вывести параметры, выполнить скрипт и перейти в REPL."""
        self.print_config()
        if self.script_path and not self.run_script():
            self.exit_code = EXIT_ERROR
            return self.exit_code
        return super().run()


def build_parser():
    """Парсер параметров командной строки эмулятора."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной строки UNIX-подобной ОС")
    parser.add_argument("--vfs", default=None,
                        help="путь к физическому расположению VFS (CSV)")
    parser.add_argument("--prompt", default=None,
                        help="пользовательское приглашение к вводу")
    parser.add_argument("--script", default=None,
                        help="путь к стартовому скрипту")
    return parser


def main(emulator_class=Emulator2, argv=None):
    """Разобрать параметры и запустить эмулятор указанного класса."""
    args = build_parser().parse_args(argv)
    emulator = emulator_class(vfs_path=args.vfs, custom_prompt=args.prompt,
                              script_path=args.script)
    return emulator.run()


if __name__ == "__main__":
    sys.exit(main())
