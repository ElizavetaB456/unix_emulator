"""Тесты для Emulator1 (этап 1)."""
from src.stage1 import Emulator1


class TestEmulator1:
    """Тесты базового эмулятора."""

    def test_init(self):
        """Проверка инициализации."""
        em = Emulator1()
        assert em.username is not None
        assert em.hostname is not None

    def test_get_prompt(self):
        """Проверка форматирования приглашения."""
        em = Emulator1()
        prompt = em.get_prompt()
        assert "$ " in prompt
        assert "@" in prompt

    def test_parse_empty_input(self):
        """Парсинг пустого ввода."""
        em = Emulator1()
        assert em.parse_and_expand("") == []

    def test_parse_simple_command(self):
        """Парсинг простой команды."""
        em = Emulator1()
        tokens = em.parse_and_expand("ls -la")
        assert tokens == ["ls", "-la"]

    def test_parse_with_quotes(self):
        """Парсинг команды с кавычками."""
        em = Emulator1()
        tokens = em.parse_and_expand('echo "hello world"')
        assert tokens == ["echo", "hello world"]

    def test_parse_syntax_error(self, capsys):
        """Обработка синтаксической ошибки в кавычках."""
        em = Emulator1()
        tokens = em.parse_and_expand('echo "unclosed')
        assert tokens == []
        captured = capsys.readouterr()
        assert "Syntax error" in captured.out
