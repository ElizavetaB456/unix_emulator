"""Общие фикстуры для тестов."""
import sys
import os

# Добавляем корень проекта в sys.path для импорта из src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


import pytest


@pytest.fixture
def tmp_vfs(tmp_path):
    """Создаёт временный CSV-файл виртуальной файловой системы."""
    vfs_file = tmp_path / "vfs.csv"
    vfs_file.write_text(
        "path,type,content\n"
        "/,dir,\n"
        "/home,dir,\n"
        "/home/user,dir,\n"
        "/home/user/file.txt,file,Hello\n"
        "/etc,dir,\n"
        "/etc/config,file,config_data\n",
        encoding="utf-8"
    )
    return str(vfs_file)


@pytest.fixture
def tmp_script(tmp_path):
    """Создаёт временный скрипт запуска."""
    script_file = tmp_path / "startup.sh"
    script_file.write_text(
        "# Comment line\n"
        "ls\n"
        "who\n",
        encoding="utf-8"
    )
    return str(script_file)
