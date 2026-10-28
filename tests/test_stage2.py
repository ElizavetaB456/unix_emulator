"""Тесты этапа 2: параметры, conf-dump, стартовый скрипт."""

from src.stage2 import Emulator2, build_parser

EXPECTED_HISTORY_LENGTH = 2
SCRIPT_ERROR_LINE = 2


class TestEmulator2:
    """Тесты эмулятора с конфигурацией."""

    def test_init_defaults(self):
        """Без параметров все значения не заданы."""
        em = Emulator2()
        assert em.vfs_path is None
        assert em.custom_prompt is None
        assert em.script_path is None
        assert em.history == []

    def test_parse_args(self):
        """Все параметры командной строки разбираются."""
        args = build_parser().parse_args(
            ["--vfs", "v.csv", "--prompt", "> ", "--script", "s.txt"])
        assert (args.vfs, args.prompt, args.script) == \
            ("v.csv", "> ", "s.txt")

    def test_get_prompt_custom(self):
        """Пользовательское приглашение."""
        assert Emulator2(custom_prompt="custom> ").get_prompt() == "custom> "

    def test_get_prompt_default(self):
        """Стандартное приглашение, если своё не задано."""
        assert Emulator2().get_prompt().endswith(":~$ ")

    def test_history_tracking(self):
        """Введённые строки попадают в историю."""
        em = Emulator2()
        em.handle_line("ls")
        em.handle_line("cd /")
        assert len(em.history) == EXPECTED_HISTORY_LENGTH

    def test_conf_dump(self, capsys):
        """conf-dump выводит параметры в формате ключ=значение."""
        em = Emulator2(vfs_path="/test", custom_prompt="p> ",
                       script_path="/s")
        assert em.handle_line("conf-dump")
        out = capsys.readouterr().out
        assert "vfs_path=/test" in out
        assert "custom_prompt=p> " in out
        assert "script_path=/s" in out

    def test_conf_dump_args(self, capsys):
        """conf-dump не принимает аргументов."""
        assert not Emulator2().handle_line("conf-dump x")
        assert "too many arguments" in capsys.readouterr().out

    def test_script_echo(self, tmp_script, capsys):
        """Команды скрипта выводятся вместе с приглашением."""
        em = Emulator2(custom_prompt="$ ", script_path=tmp_script)
        assert em.run_script()
        out = capsys.readouterr().out
        assert "$ conf-dump" in out
        assert "$ ls" in out

    def test_script_stops_on_error(self, bad_script, capsys):
        """Скрипт останавливается на первой ошибке."""
        em = Emulator2(script_path=bad_script)
        assert not em.run_script()
        out = capsys.readouterr().out
        assert f"stopped at line {SCRIPT_ERROR_LINE}" in out
        assert out.count("ls: stub") == 1

    def test_script_missing(self, capsys):
        """Отсутствующий скрипт - ошибка."""
        em = Emulator2(script_path="/no/such/script.txt")
        assert em.run() == 1
        assert "cannot read" in capsys.readouterr().out
