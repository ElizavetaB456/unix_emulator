"""Тесты для Emulator3 (этап 3)."""
from src.stage3 import Emulator3


class TestEmulator3:
    """Тесты эмулятора с VFS."""

    def test_init_no_vfs(self):
        """Инициализация без VFS."""
        em = Emulator3()
        assert em.vfs == {}
        assert em.cwd == "/"

    def test_load_vfs(self, tmp_vfs):
        """Загрузка VFS из CSV."""
        em = Emulator3(vfs_path=tmp_vfs)
        assert "/" in em.vfs
        assert "/home" in em.vfs
        assert "/home/user/file.txt" in em.vfs
        assert em.vfs["/home"]["type"] == "dir"
        assert em.vfs["/home/user/file.txt"]["type"] == "file"

    def test_resolve_path_absolute(self, tmp_vfs):
        """Разрешение абсолютного пути."""
        em = Emulator3(vfs_path=tmp_vfs)
        assert em.resolve_path("/etc") == "/etc"

    def test_resolve_path_relative(self, tmp_vfs):
        """Разрешение относительного пути."""
        em = Emulator3(vfs_path=tmp_vfs)
        em.cwd = "/home"
        assert em.resolve_path("user") == "/home/user"

    def test_resolve_path_empty(self, tmp_vfs):
        """Разрешение пустого пути."""
        em = Emulator3(vfs_path=tmp_vfs)
        em.cwd = "/home"
        assert em.resolve_path("") == "/home"

    def test_resolve_path_root(self, tmp_vfs):
        """Разрешение пути от корня."""
        em = Emulator3(vfs_path=tmp_vfs)
        em.cwd = "/"
        assert em.resolve_path("home") == "/home"

    def test_vfs_item_count(self, tmp_vfs):
        """Количество элементов в VFS."""
        em = Emulator3(vfs_path=tmp_vfs)
        assert len(em.vfs) >= 5
