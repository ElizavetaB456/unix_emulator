"""Эмулятор командной строки. Вариант 3. Этап 5: команды mkdir и mv.

Команды изменяют только представление VFS в памяти; исходный CSV-файл
не изменяется.
"""

import sys

from src.stage3 import DIR, base_name, main as run_main, normalize_path, \
    parent_of
from src.stage4 import Emulator4

MIN_MV_OPERANDS = 2


class Emulator5(Emulator4):
    """Эмулятор с командами mkdir и mv, изменяющими VFS в памяти."""

    def get_commands(self):
        """Добавить команды mkdir и mv."""
        commands = super().get_commands()
        commands.update({"mkdir": self.cmd_mkdir, "mv": self.cmd_mv})
        return commands

    def _make_dir(self, arg, parents):
        """Создать один каталог; parents - режим -p."""
        path = self.resolve_path(arg)
        if self.exists(path):
            if parents and self.is_dir(path):
                return True
            print(f"mkdir: cannot create directory '{arg}': File exists")
            return False
        parent = parent_of(path)
        if not self.exists(parent) and parents:
            if not self._make_dir(parent, parents):
                return False
        if not self.exists(parent):
            print(f"mkdir: cannot create directory '{arg}': "
                  "No such file or directory")
            return False
        if not self.is_dir(parent):
            print(f"mkdir: cannot create directory '{arg}': "
                  "Not a directory")
            return False
        self.vfs[path] = {"type": DIR, "content": b""}
        return True

    def cmd_mkdir(self, args):
        """mkdir [-p] каталог ... - создать каталоги."""
        parents = "-p" in args
        operands = [arg for arg in args if arg != "-p"]
        for arg in operands:
            if arg.startswith("-"):
                print(f"mkdir: invalid option -- '{arg[1:]}'")
                return False
        if not operands:
            print("mkdir: missing operand")
            return False
        results = [self._make_dir(arg, parents) for arg in operands]
        return all(results)

    def _rename_tree(self, src, dst):
        """Переименовать элемент и всех его потомков в словаре VFS."""
        prefix = src + "/"
        for path in sorted(self.vfs):
            if path == src or path.startswith(prefix):
                self.vfs[dst + path[len(src):]] = self.vfs.pop(path)

    def _check_target(self, src, dst, dst_arg):
        """Проверить, можно ли переместить src в dst. Текст ошибки/None."""
        if dst == src:
            return "are the same file"
        if dst.startswith(src + "/"):
            return "cannot move to a subdirectory of itself"
        parent = parent_of(dst)
        if not self.is_dir(parent):
            return f"cannot move to '{dst_arg}': No such file or directory"
        if not self.exists(dst):
            return None
        if self.is_dir(dst) and not self.is_dir(src):
            return f"cannot overwrite directory '{dst_arg}' " \
                   "with non-directory"
        if self.is_dir(src) and not self.is_dir(dst):
            return f"cannot overwrite non-directory '{dst_arg}' " \
                   "with directory"
        if self.list_dir(dst):
            return f"cannot move: '{dst_arg}': Directory not empty"
        return None

    def _move_one(self, src_arg, dst_arg):
        """Переместить или переименовать один элемент."""
        src = self.resolve_path(src_arg)
        if not self.exists(src) or src == "/":
            print(f"mv: cannot stat '{src_arg}': No such file or directory")
            return False
        dst = self.resolve_path(dst_arg)
        if self.is_dir(dst) and dst != src:
            dst = normalize_path(dst + "/" + base_name(src))
        problem = self._check_target(src, dst, dst_arg)
        if problem:
            print(f"mv: '{src_arg}': {problem}")
            return False
        self.vfs.pop(dst, None)
        self._rename_tree(src, dst)
        if self.cwd == src or self.cwd.startswith(src + "/"):
            self.cwd = dst + self.cwd[len(src):]
        return True

    def cmd_mv(self, args):
        """mv источник назначение | mv источник ... каталог."""
        if len(args) < MIN_MV_OPERANDS:
            print("mv: missing file operand")
            return False
        *sources, target = args
        if len(sources) > 1 and not self.is_dir(self.resolve_path(target)):
            print(f"mv: target '{target}' is not a directory")
            return False
        results = [self._move_one(src, target) for src in sources]
        return all(results)


def main(argv=None):
    """Запустить эмулятор этапа 5."""
    return run_main(Emulator5, argv)


if __name__ == "__main__":
    sys.exit(main())
