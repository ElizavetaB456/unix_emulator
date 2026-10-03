"""Эмулятор командной строки UNIX-подобной ОС. Вариант №3. Этап 1."""
import os
import sys
import getpass
import socket
import shlex


class Emulator1:
    """Базовый эмулятор с REPL интерфейсом."""

    def __init__(self):
        """Инициализация эмулятора."""
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()

    def get_prompt(self):
        """Возвращает приглашение ввода."""
        return f"{self.username}@{self.hostname}:~$ "

    def parse_and_expand(self, user_input):
        """Парсит ввод и раскрывает переменные окружения."""
        if not user_input:
            return []
        expanded = os.path.expandvars(user_input)
        try:
            return shlex.split(expanded)
        except ValueError:
            print("Syntax error in quotes")
            return []

    def run(self):
        """Главный цикл REPL."""
        while True:
            try:
                prompt = self.get_prompt()
                user_input = input(f"{prompt}").strip()
                if not user_input:
                    continue
                tokens = self.parse_and_expand(user_input)
                if not tokens:
                    continue
                cmd = tokens[0]
                args = tokens[1:]
                if cmd == "exit":
                    if args:
                        print("exit: too many arguments")
                        continue
                    print("Exiting emulator...")
                    sys.exit(0)
                elif cmd in ["ls", "cd"]:
                    print(f"[Stub] Command: {cmd}, "
                          f"Arguments: {args}")
                else:
                    print(f"{cmd}: command not found")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting emulator...")
                break


if __name__ == "__main__":
    emulator = Emulator1()
    emulator.run()
