"""Тесты для Emulator4 (этап 4)."""
from src.stage4 import Emulator4


class TestEmulator4:
    """Тесты эмулятора с командами."""

    def test_cmd_ls_root(self, tmp_vfs, capsys):
        """ls в корневой директории."""
        em = Emulator4(vfs_path=tmp_vfs)
        result = em.cmd_ls([])
        assert result is True
        captured = capsys.readouterr()
        assert "home" in captured.out
        assert "etc" in captured.out

    def test_cmd_ls_subdir(self, tmp_vfs, capsys):
        """ls в поддиректории."""
        em = Emulator4(vfs_path=tmp_vfs)
        result = em.cmd_ls(["/home"])
        assert result is True
        captured = capsys.readouterr()
        assert "user" in captured.out

    def test_cmd_ls_nonexistent(self, tmp_vfs, capsys):
        """ls несуществующей директории."""
        em = Emulator4(vfs_path=tmp_vfs)
        result = em.cmd_ls(["/nonexistent"])
        assert result is False
        captured = capsys.readouterr()
        assert "cannot access" in captured.out

    def test_cmd_cd_valid(self, tmp_vfs):
        """cd в существующую директорию."""
        em = Emulator4(vfs_path=tmp_vfs)
        result = em.cmd_cd(["/home"])
        assert result is True
        assert em.cwd == "/home"

    def test_cmd_cd_invalid(self, tmp_vfs, capsys):
        """cd в несуществующую директорию."""
        em = Emulator4(vfs_path=tmp_vfs)
        result = em.cmd_cd(["/nonexistent"])
        assert result is False
        assert em.cwd == "/"

    def test_cmd_cd_no_args(self, tmp_vfs):
        """cd без аргументов — переход в корень."""
        em = Emulator4(vfs_path=tmp_vfs)
        em.cwd = "/home"
        result = em.cmd_cd([])
        assert result is True
        assert em.cwd == "/"

    def test_cmd_who(self, capsys):
        """Команда who."""
        em = Emulator4()
        result = em.cmd_who([])
        assert result is True
        captured = capsys.readouterr()
        assert em.username in captured.out

    def test_cmd_cal(self, capsys):
        """Команда cal."""
        em = Emulator4()
        result = em.cmd_cal([])
        assert result is True

    def test_cmd_history(self, capsys):
        """Команда history."""
        em = Emulator4()
        em.history = ["ls", "cd /home", "who"]
        result = em.cmd_history([])
        assert result is True
        captured = capsys.readouterr()
        assert "ls" in captured.out
        assert "cd /home" in captured.out
