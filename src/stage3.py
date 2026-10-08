"""Эмулятор командной строки. Этап 3: VFS из CSV."""
import os
import sys
import argparse
import csv
import base64
import getpass
import socket
import shlex
MIN_CSV_COLUMNS=2

class Emulator3:
    """Эмулятор с поддержкой VFS из CSV."""

    def __init__(self, vfs_path=None, custom_prompt=None,
                 script_path=None):
        """Инициализация эмулятора."""
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.vfs_path = vfs_path
        self.custom_prompt = custom_prompt
        self.script_path = script_path
        self.history = []
        self.vfs = {}
        self.cwd = "/"
        if self.vfs_path:
            self.load_vfs()

    def get_prompt(self):
        """Возвращает приглашение ввода."""
        if self.custom_prompt:
            return self.custom_prompt
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

    def load_vfs(self):
        """Загружает VFS из CSV-файла."""
        try:
            with open(self.vfs_path, 'r',
                      encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or row[0].startswith('path'):
                        continue
                    path = row[0]
                    item_type = row[1]
                    content = row[2] if len(row) > MIN_CSV_COLUMNS else ""
                    self.vfs[path] = {
                        'type': item_type,
                        'content': content
                    }
            if "/" not in self.vfs:
                self.vfs["/"] = {
                    'type': 'dir',
                    'content': ''
                }
        except Exception as e:
            print(f"Error loading VFS CSV file: {e}")
            sys.exit(1)

    def resolve_path(self, target_path):
        """Преобразует путь в абсолютный."""
        if not target_path:
            return self.cwd
        if target_path.startswith("/"):
            absolute = target_path
        else:
            if self.cwd == "/":
                absolute = "/" + target_path
            else:
                absolute = self.cwd + "/" + target_path
        parts = []
        for part in absolute.split("/"):
            if part == "." and parts:
                parts.pop()
            elif part and part != ".":
                parts.append(part)
        return "/" + "/".join(parts)

    def execute_command(self, tokens):
        """Выполняет команду."""
        if not tokens:
            return True
        cmd = tokens[0]
        args = tokens[1:]
        self.history.append(" ".join(tokens))

        if cmd == "exit":
            print("Exiting emulator...")
            sys.exit(0)
        elif cmd == "conf-dump":
            print(f"vfs_path: {self.vfs_path}")
            print(f"custom_prompt: {self.custom_prompt}")
            print(f"script_path: {self.script_path}")
            return True
        elif cmd in ["ls", "cd"]:
            print(f"[Stub] Command: {cmd}, "
                  f"Arguments: {args}")
            return True
        else:
            print(f"{cmd}: command not found")
            return False

    def run_script(self):
        """Выполняет команды из стартового скрипта."""
        if not os.path.exists(self.script_path):
            print(f"Error: Script file "
                  f"'{self.script_path}' not found")
            sys.exit(1)

        with open(self.script_path, 'r',
                  encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                print(f"{self.get_prompt()}{line}")
                tokens = self.parse_and_expand(line)
                success = self.execute_command(tokens)
                if not success:
                    print("Script execution halted "
                          "due to an error.")
                    sys.exit(1)

    def run(self):
        """Главный цикл эмулятора."""
        print("---Emulator Configuration---")
        print(f"VFS Path: {self.vfs_path}")
        print(f"Custom Prompt: {self.custom_prompt}")
        print(f"Script Path: {self.script_path}")
        print(f"VFS loaded: {len(self.vfs)} items")
        print("-------------")

        if self.script_path:
            self.run_script()

        while True:
            try:
                user_input = input(
                    f"{self.get_prompt()}").strip()
                tokens = self.parse_and_expand(
                    user_input)
                self.execute_command(tokens)
            except (KeyboardInterrupt, EOFError):
                break


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", default=None)
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--script", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    emulator = Emulator3(
        vfs_path=args.vfs,
        custom_prompt=args.prompt,
        script_path=args.script
    )
    emulator.run()
