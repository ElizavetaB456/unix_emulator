"""Тесты этапа 3: загрузка VFS из CSV."""

import pytest

from src.stage3 import Emulator3, VFSError, load_vfs, normalize_path

VFS_ITEMS = 7
BINARY = b"\x00\x01\x02\xff"


class TestLoadVFS:
    """Загрузка и проверка CSV-файла VFS."""

    def test_load(self, tmp_vfs):
        """Каталоги и файлы загружаются в память."""
        vfs = load_vfs(tmp_vfs)
        assert len(vfs) == VFS_ITEMS
        assert vfs["/home"]["type"] == "dir"
        assert vfs["/home/user/file.txt"]["content"] == b"Hello"

    def test_base64(self, tmp_vfs):
        """Двоичные данные декодируются из base64."""
        assert load_vfs(tmp_vfs)["/home/user/logo.bin"]["content"] == BINARY

    def test_errors(self, tmp_path):
        """Ошибки формата CSV обнаруживаются."""
        bad_rows = {
            "мало столбцов": "/a\n",
            "относительный путь": "a,dir,,\n",
            "неизвестный тип": "/a,link,,\n",
            "некорректный base64": "/a,file,@@@,base64\n",
            "неизвестная кодировка": "/a,file,x,utf-16\n",
            "нет родительского каталога": "/a/b,file,x,\n",
            "повторяющийся путь": "/a,dir,,\n/a,dir,,\n",
        }
        for number, rows in enumerate(bad_rows.values()):
            path = tmp_path / f"bad{number}.csv"
            path.write_text("path,type,content,encoding\n" + rows,
                            encoding="utf-8")
            with pytest.raises(VFSError):
                load_vfs(str(path))

    def test_missing_file(self):
        """Отсутствующий файл VFS - ошибка."""
        with pytest.raises(VFSError):
            load_vfs("/no/such/vfs.csv")


class TestEmulator3:
    """Эмулятор с VFS."""

    def test_init_no_vfs(self):
        """Без VFS есть только корневой каталог."""
        em = Emulator3()
        assert list(em.vfs) == ["/"]
        assert em.cwd == "/"

    def test_normalize(self):
        """Обработка . и .. в путях."""
        assert normalize_path("/a/./b/../c//d") == "/a/c/d"
        assert normalize_path("/../..") == "/"

    def test_resolve_path(self, tmp_vfs):
        """Абсолютные и относительные пути."""
        em = Emulator3(vfs_path=tmp_vfs)
        em.cwd = "/home/user"
        assert em.resolve_path("/etc") == "/etc"
        assert em.resolve_path("file.txt") == "/home/user/file.txt"
        assert em.resolve_path("..") == "/home"
        assert em.resolve_path("../../etc") == "/etc"
        assert em.resolve_path("") == "/home/user"

    def test_list_dir(self, tmp_vfs):
        """Содержимое каталога."""
        em = Emulator3(vfs_path=tmp_vfs)
        assert em.list_dir("/") == ["etc", "home"]
        assert em.list_dir("/home/user") == ["file.txt", "logo.bin"]

    def test_conf_dump_vfs(self, tmp_vfs, capsys):
        """conf-dump сообщает число элементов VFS."""
        Emulator3(vfs_path=tmp_vfs).handle_line("conf-dump")
        assert f"vfs_items={VFS_ITEMS}" in capsys.readouterr().out

    def test_csv_not_modified(self, tmp_vfs):
        """CSV-файл VFS не изменяется."""
        before = open(tmp_vfs, encoding="utf-8").read()
        Emulator3(vfs_path=tmp_vfs).handle_line("ls")
        assert open(tmp_vfs, encoding="utf-8").read() == before
