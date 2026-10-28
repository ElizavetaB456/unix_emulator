"""Эмулятор командной строки UNIX-подобной ОС. Вариант 3. Этап 1: REPL.

Минимальный прототип: приглашение к вводу строится по реальным данным
ОС (имя пользователя и имя компьютера), парсер раскрывает переменные
окружения ($HOME, ${USER}), команды ls и cd - заглушки, exit завершает
работу.
"""

import functools
import getpass
import os
import shlex
import socket
import sys

EXIT_OK = 0
EXIT_ERROR = 1


class Emulator1:
    """REPL-эмулятор с заглушками ls, cd и командой exit."""

    def __init__(self):
        """Определить пользователя и компьютер, подготовить состояние."""
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.history = []
        self.running = True
        self.exit_code = EXIT_OK

    def prompt_path(self):
        """Текущий каталог для приглашения (на этом этапе всегда ~)."""
        return "~"

    def get_prompt(self):
        """Приглашение к вводу вида username@hostname:~$ ."""
        return f"{self.username}@{self.hostname}:{self.prompt_path()}$ "

    def parse_and_expand(self, user_input):
        """Раскрыть переменные окружения и разбить строку на слова.

        Возвращает список слов или None при синтаксической ошибке
        (например, незакрытая кавычка).
        """
        expanded = os.path.expandvars(user_input)
        try:
            return shlex.split(expanded)
        except ValueError as error:
            print(f"syntax error: {error}")
            return None

    def get_commands(self):
        """Таблица команд: имя -> обработчик, принимающий аргументы."""
        return {
            "exit": self.cmd_exit,
            "ls": functools.partial(self.cmd_stub, "ls"),
            "cd": functools.partial(self.cmd_stub, "cd"),
        }

    def cmd_stub(self, name, args):
        """Заглушка: вывести имя команды и её аргументы."""
        print(f"{name}: stub, arguments: {args}")
        return True

    def cmd_exit(self, args):
        """Завершить работу эмулятора: exit [код]."""
        if len(args) > 1:
            print("exit: too many arguments")
            return False
        if args and not args[0].lstrip("-").isdigit():
            print(f"exit: {args[0]}: numeric argument required")
            return False
        self.exit_code = int(args[0]) if args else EXIT_OK
        self.running = False
        return True

    def execute_command(self, tokens):
        """Выполнить разобранную команду. Возвращает True при успехе."""
        if tokens is None:
            return False
        if not tokens:
            return True
        name, args = tokens[0], tokens[1:]
        handler = self.get_commands().get(name)
        if handler is None:
            print(f"{name}: command not found")
            return False
        return handler(args)

    def handle_line(self, line):
        """Обработать одну строку ввода: история, разбор, выполнение."""
        line = line.strip()
        if not line:
            return True
        self.history.append(line)
        return self.execute_command(self.parse_and_expand(line))

    def run(self):
        """Главный цикл REPL. Возвращает код завершения."""
        while self.running:
            try:
                line = input(self.get_prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.handle_line(line)
        return self.exit_code


def main():
    """Запустить эмулятор этапа 1."""
    return Emulator1().run()


if __name__ == "__main__":
    sys.exit(main())
