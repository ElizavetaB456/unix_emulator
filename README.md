# Эмулятор командной строки UNIX-подобной ОС

Эмулятор командной строки, разработанный в 5 этапов. Каждый этап расширяет функциональность предыдущего.

## Этапы разработки

| Этап | Класс    | Описание                                         |
|------|----------|--------------------------------------------------|
| 1    | Emulator1 | Базовый REPL-интерфейс                           |
| 2    | Emulator2 | Конфигурация через аргументы, стартовые скрипты   |
| 3    | Emulator3 | Виртуальная файловая система (VFS) из CSV         |
| 4    | Emulator4 | Команды: ls, cd, history, cal, who                |
| 5    | Emulator5 | Полнофункциональный: добавлены mkdir, mv          |

## Структура репозитория

```
.
├── src/                # Исходный код
│   ├── __init__.py
│   ├── stage1.py       # Этап 1 — базовый REPL
│   ├── stage2.py       # Этап 2 — конфигурация и скрипты
│   ├── stage3.py       # Этап 3 — VFS из CSV
│   ├── stage4.py       # Этап 4 — основные команды
│   └── stage5.py       # Этап 5 — полнофункциональный эмулятор
├── tests/              # Тесты
│   ├── __init__.py
│   ├── conftest.py     # Общие фикстуры
│   ├── test_stage1.py  # Тесты этапа 1
│   ├── test_stage2.py  # Тесты этапа 2
│   ├── test_stage3.py  # Тесты этапа 3
│   ├── test_stage4.py  # Тесты этапа 4
│   └── test_stage5.py  # Тесты этапа 5
├── .gitignore
├── Makefile
├── README.md
└── requirements.txt
```

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

### Этап 1
```bash
python -m src.stage1
```

### Этапы 2–5 (с параметрами)
```bash
python -m src.stage2 --vfs vfs.csv --prompt "my> " --script startup.sh
python -m src.stage3 --vfs vfs.csv --prompt "my> "
python -m src.stage4 --vfs vfs.csv --prompt "my> "
python -m src.stage5 --vfs vfs.csv --prompt "my> " --script startup.sh
```

### Через Makefile
```bash
make run STAGE=5 VFS=vfs.csv PROMPT="my> " SCRIPT=startup.sh
```

## Поддерживаемые команды (этап 5)

| Команда    | Описание                              |
|-----------|---------------------------------------|
| `ls`     | Вывод содержимого директории           |
| `cd`     | Смена текущей директории               |
| `mkdir`  | Создание директории                    |
| `mv`     | Перемещение / переименование          |
| `history`| История команд                        |
| `cal`    | Календарь текущего месяца             |
| `who`    | Имя текущего пользователя             |
| `conf-dump` | Вывод конфигурации эмулятора       |
| `exit`   | Выход                                |

## Тесты

```bash
make test
# или
pytest tests/ -v
```

## Формат VFS

Виртуальная файловая система загружается из CSV-файла со столбцами:

```
path,type,content
/,dir,
/home,dir,
/home/user/file.txt,file,Hello World
```

## Лицензия

MIT
