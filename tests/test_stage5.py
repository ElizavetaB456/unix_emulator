"""Тесты для Emulator5 (этап 5)."""
from src.stage5 import Emulator5


class TestEmulator5:
    """Тесты полнофункционального эмулятора."""

    def test_cmd_mkdir_valid(self, tmp_vfs):
        """Создание новой директории."""
        em = Emulator5(vfs_path=tmp_vfs)
        result = em.cmd_mkdir(["/home/newdir"])
        assert result is True
        assert "/home/newdir" in em.vfs
        assert em.vfs["/home/newdir"]["type"] == "dir"

    def test_cmd_mkdir_no_args(self, capsys):
        """mkdir без аргументов."""
        em = Emulator5()
        result = em.cmd_mkdir([])
        assert result is False
        captured = capsys.readouterr()
        assert "missing operand" in captured.out

    def test_cmd_mkdir_exists(self, tmp_vfs, capsys):
        """mkdir уже существующей директории."""
        em = Emulator5(vfs_path=tmp_vfs)
        result = em.cmd_mkdir(["/home"])
        assert result is False
        captured = capsys.readouterr()
        assert "File exists" in captured.out

    def test_cmd_mkdir_no_parent(self, tmp_vfs, capsys):
        """mkdir с несуществующим родителем."""
        em = Emulator5(vfs_path=tmp_vfs)
        result = em.cmd_mkdir(["/nonexistent/subdir"])
        assert result is False
        captured = capsys.readouterr()
        assert "No such directory" in captured.out

    def test_cmd_mv_rename(self, tmp_vfs):
        """Переименование файла."""
        em = Emulator5(vfs_path=tmp_vfs)
        result = em.cmd_mv(["/home/user/file.txt", "/home/user/renamed.txt"])
        assert result is True
        assert "/home/user/file.txt" not in em.vfs
        assert "/home/user/renamed.txt" in em.vfs

    def test_cmd_mv_no_args(self, capsys):
        """mv без аргументов."""
        em = Emulator5()
        result = em.cmd_mv([])
        assert result is False
        captured = capsys.readouterr()
        assert "missing file operand" in captured.out

    def test_cmd_mv_nonexistent_src(self, tmp_vfs, capsys):
        """mv несуществующего источника."""
        em = Emulator5(vfs_path=tmp_vfs)
        result = em.cmd_mv(["/nonexistent", "/home"])
        assert result is False
        captured = capsys.readouterr()
        assert "cannot stat" in captured.out

    def test_cmd_mv_into_dir(self, tmp_vfs):
        """Перемещение файла в директорию."""
        em = Emulator5(vfs_path=tmp_vfs)
        result = em.cmd_mv(["/etc/config", "/home"])
        assert result is True
        assert "/etc/config" not in em.vfs
        assert "/home/config" in em.vfs

    def test_cmd_mv_one_arg(self, capsys):
        """mv с одним аргументом."""
        em = Emulator5()
        result = em.cmd_mv(["/path"])
        assert result is False
        captured = capsys.readouterr()
        assert "missing file operand" in captured.out
