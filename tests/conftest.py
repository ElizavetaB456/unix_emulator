"""Общие фикстуры для тестов эмулятора.

Корень проекта добавляется в путь импорта настройкой pythonpath
в файле pytest.ini, поэтому тесты импортируют модули как src.stageN.
"""

import pytest


@pytest.fixture
def tmp_vfs(tmp_path):
    """Временный CSV-файл VFS с тремя уровнями вложенности."""
    vfs_file = tmp_path / "vfs.csv"
    vfs_file.write_text(
        "path,type,content,encoding\n"
        "/,dir,,\n"
        "/home,dir,,\n"
        "/home/user,dir,,\n"
        "/home/user/file.txt,file,Hello,text\n"
        "/home/user/logo.bin,file,AAEC/w==,base64\n"
        "/etc,dir,,\n"
        "/etc/config,file,config_data,\n",
        encoding="utf-8",
    )
    return str(vfs_file)


@pytest.fixture
def tmp_script(tmp_path):
    """Временный стартовый скрипт без ошибок."""
    script_file = tmp_path / "startup.txt"
    script_file.write_text("# comment\n\nconf-dump\nls\n", encoding="utf-8")
    return str(script_file)


@pytest.fixture
def bad_script(tmp_path):
    """Стартовый скрипт с ошибкой во второй команде."""
    script_file = tmp_path / "bad.txt"
    script_file.write_text("ls\nunknown-cmd\nls\n", encoding="utf-8")
    return str(script_file)
