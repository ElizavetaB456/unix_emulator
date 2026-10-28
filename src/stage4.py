"""Эмулятор командной строки. Вариант 3. Этап 4: основные команды.

Реализована логика ls и cd по VFS, добавлены команды history, cal, who.
Приглашение показывает текущий каталог VFS.
"""

import calendar
import sys
from datetime import datetime

from src.stage3 import Emulator3, main as run_main

MIN_MONTH, MAX_MONTH = 1, 12
MIN_YEAR, MAX_YEAR = 1, 9999
MAX_CAL_ARGS = 2


def _parse_int(text, low, high):
    """Целое число в диапазоне [low, high] или None."""
    if not text.isdigit():
        return None
    value = int(text)
    return value if low <= value <= high else None


class Emulator4(Emulator3):
    """Эмулятор с командами ls, cd, history, cal, who."""

    def __init__(self, vfs_path=None, custom_prompt=None,
                 script_path=None):
        """Запомнить время входа для команды who."""
        super().__init__(vfs_path, custom_prompt, script_path)
        self.login_time = datetime.now()

    def prompt_path(self):
        """Текущий каталог VFS в приглашении."""
        return self.cwd

    def get_commands(self):
        """Заменить заглушки ls и cd и добавить новые команды."""
        commands = super().get_commands()
        commands.update({
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "history": self.cmd_history,
            "cal": self.cmd_cal,
            "who": self.cmd_who,
        })
        return commands

    def _ls_one(self, arg, show_header):
        """Вывести содержимое одного каталога или имя файла."""
        path = self.resolve_path(arg)
        if not self.exists(path):
            print(f"ls: cannot access '{arg}': No such file or directory")
            return False
        if not self.is_dir(path):
            print(arg)
            return True
        if show_header:
            print(f"{arg}:")
        names = self.list_dir(path)
        if names:
            print("  ".join(names))
        return True

    def cmd_ls(self, args):
        """ls [путь ...] - содержимое каталогов (по умолчанию текущего)."""
        for arg in args:
            if arg.startswith("-") and len(arg) > 1:
                print(f"ls: invalid option -- '{arg[1:]}'")
                return False
        targets = args or [self.cwd]
        results = [self._ls_one(arg, len(targets) > 1) for arg in targets]
        return all(results)

    def cmd_cd(self, args):
        """cd [каталог] - сменить текущий каталог (без аргумента - /)."""
        if len(args) > 1:
            print("cd: too many arguments")
            return False
        path = self.resolve_path(args[0]) if args else "/"
        if not self.exists(path):
            print(f"cd: no such file or directory: {args[0]}")
            return False
        if not self.is_dir(path):
            print(f"cd: not a directory: {args[0]}")
            return False
        self.cwd = path
        return True

    def cmd_history(self, args):
        """history [n] - последние n команд (по умолчанию все)."""
        if len(args) > 1:
            print("history: too many arguments")
            return False
        count = len(self.history)
        if args:
            if not args[0].isdigit():
                print(f"history: {args[0]}: numeric argument required")
                return False
            count = min(int(args[0]), count)
        start = len(self.history) - count
        for number in range(start, len(self.history)):
            print(f"{number + 1:5}  {self.history[number]}")
        return True

    def cmd_cal(self, args):
        """cal [[месяц] год] - календарь на месяц или на год."""
        today = datetime.now()
        if not args:
            print(calendar.month(today.year, today.month))
            return True
        if len(args) > MAX_CAL_ARGS:
            print("cal: too many arguments")
            return False
        year = _parse_int(args[-1], MIN_YEAR, MAX_YEAR)
        if year is None:
            print(f"cal: invalid year '{args[-1]}'")
            return False
        if len(args) == 1:
            print(calendar.calendar(year))
            return True
        month = _parse_int(args[0], MIN_MONTH, MAX_MONTH)
        if month is None:
            print(f"cal: invalid month '{args[0]}'")
            return False
        print(calendar.month(year, month))
        return True

    def cmd_who(self, args):
        """who - кто работает в системе: пользователь, терминал, вход."""
        if args:
            print(f"who: extra operand '{args[0]}'")
            return False
        login = self.login_time.strftime("%Y-%m-%d %H:%M")
        print(f"{self.username:<12} console      {login}")
        return True


def main(argv=None):
    """Запустить эмулятор этапа 4."""
    return run_main(Emulator4, argv)


if __name__ == "__main__":
    sys.exit(main())
