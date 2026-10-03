"""Тесты для Emulator2 (этап 2)."""
from src.stage2 import Emulator2


class TestEmulator2:
    """Тесты эмулятора с конфигурацией."""

    def test_init_defaults(self):
        """Инициализация без аргументов."""
        em = Emulator2()
        assert em.vfs_path is None
        assert em.custom_prompt is None
        assert em.script_path is None
        assert em.history == []

    def test_init_with_args(self):
        """Инициализация с аргументами."""
        em = Emulator2(
            vfs_path="/tmp/vfs.csv",
            custom_prompt="test> ",
            script_path="/tmp/script.sh"
        )
        assert em.vfs_path == "/tmp/vfs.csv"
        assert em.custom_prompt == "test> "
        assert em.script_path == "/tmp/script.sh"

    def test_get_prompt_custom(self):
        """Кастомное приглашение."""
        em = Emulator2(custom_prompt="custom> ")
        assert em.get_prompt() == "custom> "

    def test_get_prompt_default(self):
        """Приглашение по умолчанию."""
        em = Emulator2()
        prompt = em.get_prompt()
        assert "$ " in prompt

    def test_execute_unknown_command(self, capsys):
        """Неизвестная команда."""
        em = Emulator2()
        result = em.execute_command(["nonexistent"])
        assert result is False
        captured = capsys.readouterr()
        assert "command not found" in captured.out

    def test_history_tracking(self):
        """История команд."""
        em = Emulator2()
        em.execute_command(["ls"])
        em.execute_command(["who"])
        assert len(em.history) == 2
        assert "ls" in em.history[0]
        assert "who" in em.history[1]

    def test_conf_dump(self, capsys):
        """Команда conf-dump."""
        em = Emulator2(vfs_path="/test", custom_prompt="p> ", script_path="/s")
        em.execute_command(["conf-dump"])
        captured = capsys.readouterr()
        assert "/test" in captured.out
        assert "p> " in captured.out
        assert "/s" in captured.out
