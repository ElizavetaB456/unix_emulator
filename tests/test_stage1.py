"""Тесты этапа 1: REPL, парсер, заглушки и exit."""

import builtins

from src.stage1 import Emulator1

EXIT_CODE = 3


class TestEmulator1:
    """Тесты базового эмулятора."""

    def test_init(self):
        """Имя пользователя и компьютера берутся из ОС."""
        em = Emulator1()
        assert em.username
        assert em.hostname

    def test_get_prompt(self):
        """Приглашение имеет вид username@hostname:~$ ."""
        em = Emulator1()
        assert em.get_prompt() == f"{em.username}@{em.hostname}:~$ "

    def test_parse_empty_input(self):
        """Пустой ввод - пустой список слов."""
        assert Emulator1().parse_and_expand("") == []

    def test_parse_simple_command(self):
        """Простая команда разбивается на слова."""
        assert Emulator1().parse_and_expand("ls -la") == ["ls", "-la"]

    def test_parse_with_quotes(self):
        """Аргумент в кавычках - одно слово."""
        tokens = Emulator1().parse_and_expand('cd "my dir"')
        assert tokens == ["cd", "my dir"]

    def test_parse_env_variables(self, monkeypatch):
        """Переменные окружения раскрываются."""
        monkeypatch.setenv("HOME", "/home/tester")
        tokens = Emulator1().parse_and_expand("cd $HOME ${HOME}/x")
        assert tokens == ["cd", "/home/tester", "/home/tester/x"]

    def test_parse_syntax_error(self, capsys):
        """Незакрытая кавычка - ошибка разбора."""
        em = Emulator1()
        assert em.parse_and_expand('ls "unclosed') is None
        assert not em.handle_line('ls "unclosed')
        assert "syntax error" in capsys.readouterr().out

    def test_stub_commands(self, capsys):
        """ls и cd выводят своё имя и аргументы."""
        em = Emulator1()
        assert em.handle_line("ls -l /tmp")
        assert em.handle_line("cd /home")
        out = capsys.readouterr().out
        assert "ls: stub, arguments: ['-l', '/tmp']" in out
        assert "cd: stub, arguments: ['/home']" in out

    def test_unknown_command(self, capsys):
        """Неизвестная команда - ошибка."""
        assert not Emulator1().handle_line("foo bar")
        assert "foo: command not found" in capsys.readouterr().out

    def test_exit(self):
        """exit останавливает REPL, exit N задаёт код."""
        em = Emulator1()
        assert em.handle_line(f"exit {EXIT_CODE}")
        assert not em.running
        assert em.exit_code == EXIT_CODE

    def test_exit_bad_args(self, capsys):
        """Неверные аргументы exit - ошибка, работа продолжается."""
        em = Emulator1()
        assert not em.handle_line("exit a")
        assert not em.handle_line("exit 1 2")
        assert em.running
        out = capsys.readouterr().out
        assert "numeric argument required" in out
        assert "too many arguments" in out

    def test_run_repl(self, monkeypatch, capsys):
        """REPL читает команды до exit."""
        lines = iter(["ls", "exit"])
        monkeypatch.setattr(builtins, "input", lambda prompt: next(lines))
        assert Emulator1().run() == 0
        assert "ls: stub" in capsys.readouterr().out
