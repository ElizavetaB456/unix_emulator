"""Тесты этапа 5: mkdir и mv."""

from src.stage5 import Emulator5


class TestMkdir:
    """Команда mkdir."""

    def test_mkdir(self, tmp_vfs):
        """Создание каталогов по абсолютному и относительному пути."""
        em = Emulator5(vfs_path=tmp_vfs)
        assert em.handle_line("mkdir /home/new")
        em.handle_line("cd /home")
        assert em.handle_line("mkdir rel other")
        assert em.is_dir("/home/new")
        assert em.is_dir("/home/rel") and em.is_dir("/home/other")

    def test_mkdir_parents(self, tmp_vfs):
        """mkdir -p создаёт промежуточные каталоги."""
        em = Emulator5(vfs_path=tmp_vfs)
        assert em.handle_line("mkdir -p /a/b/c")
        assert em.is_dir("/a") and em.is_dir("/a/b/c")
        assert em.handle_line("mkdir -p /a/b")

    def test_mkdir_errors(self, tmp_vfs, capsys):
        """Ошибки mkdir: каждая команда завершается неудачей."""
        cases = {
            "mkdir": "missing operand",
            "mkdir /home": "File exists",
            "mkdir /none/sub": "No such file or directory",
            "mkdir /etc/config/sub": "Not a directory",
            "mkdir -x /q": "invalid option",
        }
        em = Emulator5(vfs_path=tmp_vfs)
        for line, message in cases.items():
            assert not em.handle_line(line)
            assert message in capsys.readouterr().out


class TestMv:
    """Команда mv."""

    def test_rename_file(self, tmp_vfs):
        """Переименование файла."""
        em = Emulator5(vfs_path=tmp_vfs)
        assert em.handle_line("mv /home/user/file.txt /home/user/new.txt")
        assert not em.exists("/home/user/file.txt")
        assert em.vfs["/home/user/new.txt"]["content"] == b"Hello"

    def test_move_into_dir(self, tmp_vfs):
        """Перемещение файла в каталог."""
        em = Emulator5(vfs_path=tmp_vfs)
        assert em.handle_line("mv /etc/config /home")
        assert em.exists("/home/config")
        assert not em.exists("/etc/config")

    def test_move_dir_with_children(self, tmp_vfs):
        """Перемещение каталога вместе с содержимым."""
        em = Emulator5(vfs_path=tmp_vfs)
        em.handle_line("cd /home/user")
        assert em.handle_line("mv /home/user /etc/u")
        assert em.exists("/etc/u/file.txt")
        assert not em.exists("/home/user")
        assert em.cwd == "/etc/u"

    def test_move_many(self, tmp_vfs):
        """Несколько источников перемещаются в каталог."""
        em = Emulator5(vfs_path=tmp_vfs)
        em.handle_line("mkdir /dst")
        assert em.handle_line("mv /etc/config /home/user/file.txt /dst")
        assert em.list_dir("/dst") == ["config", "file.txt"]

    def test_mv_errors(self, tmp_vfs, capsys):
        """Ошибки mv: каждая команда завершается неудачей."""
        cases = {
            "mv": "missing file operand",
            "mv /home": "missing file operand",
            "mv /nonexistent /home": "cannot stat",
            "mv /home /home/user": "subdirectory of itself",
            "mv /etc/config /none/x": "No such file or directory",
            "mv /etc /home/user/file.txt": "non-directory",
            "mv /etc/config /home/x /home/user/file.txt": "not a directory",
        }
        em = Emulator5(vfs_path=tmp_vfs)
        for line, message in cases.items():
            assert not em.handle_line(line)
            assert message in capsys.readouterr().out

    def test_csv_not_modified(self, tmp_vfs):
        """Изменения выполняются только в памяти."""
        before = open(tmp_vfs, encoding="utf-8").read()
        em = Emulator5(vfs_path=tmp_vfs)
        em.handle_line("mkdir /tmp2")
        em.handle_line("mv /etc /tmp2")
        assert open(tmp_vfs, encoding="utf-8").read() == before
