"""Эмулятор командной строки. Вариант 3. Этап 3: VFS.

Виртуальная файловая система загружается из CSV-файла и целиком
хранится в памяти; сам CSV-файл не изменяется.

Формат CSV (первая строка - заголовок):

    path,type,content,encoding
    /,dir,,
    /home,dir,,
    /home/readme.txt,file,Hello,text
    /bin/logo.bin,file,iVBORw0KGgo=,base64

* path - абсолютный путь; вложенность задаётся путём: элемент
  /home/user/a.txt лежит в каталоге /home/user, который должен быть
  описан в файле;
* type - dir (каталог) или file (файл);
* content - содержимое файла (для каталогов пусто);
* encoding - text (по умолчанию) или base64 для двоичных данных.
"""

import base64
import binascii
import csv
import sys

from src.stage2 import Emulator2, main as run_main

DIR = "dir"
FILE = "file"
ENCODINGS = ("text", "base64")
MIN_COLUMNS = 2
PATH_COL, TYPE_COL, CONTENT_COL, ENCODING_COL = range(4)


class VFSError(Exception):
    """Ошибка загрузки или структуры VFS."""


def normalize_path(path):
    """Привести абсолютный путь к каноническому виду (обработать . и ..)."""
    parts = []
    for part in path.split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part and part != ".":
            parts.append(part)
    return "/" + "/".join(parts)


def parent_of(path):
    """Родительский каталог пути (для корня - сам корень)."""
    if path == "/":
        return "/"
    head = path.rsplit("/", 1)[0]
    return head or "/"


def base_name(path):
    """Последний компонент пути."""
    return path.rsplit("/", 1)[-1]


def _decode_content(row, line):
    """Получить содержимое файла в виде байтов."""
    content = row[CONTENT_COL] if len(row) > CONTENT_COL else ""
    encoding = row[ENCODING_COL] if len(row) > ENCODING_COL else ""
    encoding = encoding.strip() or "text"
    if encoding not in ENCODINGS:
        raise VFSError(f"line {line}: unknown encoding '{encoding}'")
    if encoding == "text":
        return content.encode("utf-8")
    try:
        return base64.b64decode(content, validate=True)
    except (binascii.Error, ValueError):
        raise VFSError(f"line {line}: invalid base64 data") from None


def _parse_row(row, line):
    """Разобрать строку CSV в пару (путь, узел VFS)."""
    if len(row) < MIN_COLUMNS:
        raise VFSError(f"line {line}: expected path,type[,content,encoding]")
    raw_path, kind = row[PATH_COL].strip(), row[TYPE_COL].strip()
    if not raw_path.startswith("/"):
        raise VFSError(f"line {line}: path must be absolute: '{raw_path}'")
    if kind not in (DIR, FILE):
        raise VFSError(f"line {line}: unknown type '{kind}'")
    content = _decode_content(row, line) if kind == FILE else b""
    return normalize_path(raw_path), {"type": kind, "content": content}


def _check_tree(vfs):
    """Проверить, что у каждого элемента есть родительский каталог."""
    for path in vfs:
        parent = parent_of(path)
        if path != "/" and vfs.get(parent, {}).get("type") != DIR:
            raise VFSError(f"'{path}': parent directory '{parent}' "
                           "is missing")


def _read_rows(handle, vfs):
    """Прочитать строки CSV и добавить элементы в словарь VFS."""
    for line, row in enumerate(csv.reader(handle), 1):
        if not row or (line == 1 and row[0].strip() == "path"):
            continue
        path, node = _parse_row(row, line)
        if path in vfs and path != "/":
            raise VFSError(f"line {line}: duplicate path '{path}'")
        vfs[path] = node


def load_vfs(csv_path):
    """Загрузить VFS из CSV-файла в словарь путь -> узел."""
    vfs = {"/": {"type": DIR, "content": b""}}
    try:
        with open(csv_path, encoding="utf-8", newline="") as handle:
            _read_rows(handle, vfs)
    except OSError as error:
        raise VFSError(f"cannot read '{csv_path}': {error.strerror}") \
            from None
    except csv.Error as error:
        raise VFSError(f"invalid CSV: {error}") from None
    _check_tree(vfs)
    return vfs


class Emulator3(Emulator2):
    """Эмулятор с виртуальной файловой системой в памяти."""

    def __init__(self, vfs_path=None, custom_prompt=None,
                 script_path=None):
        """Загрузить VFS (если задана) и установить текущий каталог."""
        super().__init__(vfs_path, custom_prompt, script_path)
        self.cwd = "/"
        self.vfs = load_vfs(vfs_path) if vfs_path else {
            "/": {"type": DIR, "content": b""}}

    def config_items(self):
        """Добавить к параметрам сведения о загруженной VFS."""
        return super().config_items() + [("vfs_items", len(self.vfs))]

    def resolve_path(self, target_path):
        """Преобразовать путь (абсолютный или относительный) в абсолютный."""
        if not target_path:
            return self.cwd
        if target_path.startswith("/"):
            return normalize_path(target_path)
        return normalize_path(self.cwd + "/" + target_path)

    def exists(self, path):
        """Есть ли элемент VFS по абсолютному пути."""
        return path in self.vfs

    def is_dir(self, path):
        """Является ли элемент каталогом."""
        return self.vfs.get(path, {}).get("type") == DIR

    def list_dir(self, path):
        """Отсортированные имена элементов каталога."""
        return sorted(base_name(item) for item in self.vfs
                      if item != "/" and parent_of(item) == path)


def main(emulator_class=Emulator3, argv=None):
    """Запустить эмулятор; при ошибке загрузки VFS вернуть код 1."""
    try:
        return run_main(emulator_class, argv)
    except VFSError as error:
        print(f"VFS error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
