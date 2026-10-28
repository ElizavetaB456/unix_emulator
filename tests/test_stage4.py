"""Тесты этапа 4: ls, cd, history, cal, who."""

from src.stage4 import Emulator4

HISTORY_TAIL = 2


class TestEmulator4:
    """Тесты основных команд."""

    def test_prompt_shows_cwd(self, tmp_vfs):
        """Приглашение показывает текущий каталог VFS."""
        em = Emulator4(vfs_path=tmp_vfs)
        em.handle_line("cd /home/user")
        assert em.get_prompt().endswith(":/home/user$ ")

    def test_ls_root(self, tmp_vfs, capsys):
        """ls без аргументов - содержимое текущего каталога."""
        assert Emulator4(vfs_path=tmp_vfs).handle_line("ls")
        assert capsys.readouterr().out.strip() == "etc  home"

    def test_ls_paths(self, tmp_vfs, capsys):
        """ls каталога, файла и нескольких путей."""
        em = Emulator4(vfs_path=tmp_vfs)
        assert em.handle_line("ls /home/user")
        assert em.handle_line("ls /etc/config")
        assert em.handle_line("ls /home /etc")
        out = capsys.readouterr().out
        assert "file.txt  logo.bin" in out
        assert "/etc/config" in out
        assert "/home:" in out and "/etc:" in out

    def test_ls_errors(self, tmp_vfs, capsys):
        """ls несуществующего пути и неизвестной опции."""
        em = Emulator4(vfs_path=tmp_vfs)
        assert not em.handle_line("ls /nonexistent")
        assert not em.handle_line("ls -z")
        out = capsys.readouterr().out
        assert "cannot access '/nonexistent'" in out
        assert "invalid option" in out

    def test_cd(self, tmp_vfs):
        """cd по абсолютным и относительным путям, .. и без аргумента."""
        em = Emulator4(vfs_path=tmp_vfs)
        assert em.handle_line("cd home")
        assert em.handle_line("cd user")
        assert em.cwd == "/home/user"
        assert em.handle_line("cd ..")
        assert em.cwd == "/home"
        assert em.handle_line("cd")
        assert em.cwd == "/"

    def test_cd_errors(self, tmp_vfs, capsys):
        """cd в несуществующий каталог, в файл, с лишними аргументами."""
        em = Emulator4(vfs_path=tmp_vfs)
        assert not em.handle_line("cd /nonexistent")
        assert not em.handle_line("cd /etc/config")
        assert not em.handle_line("cd / /etc")
        assert em.cwd == "/"
        out = capsys.readouterr().out
        assert "no such file or directory" in out
        assert "not a directory" in out
        assert "too many arguments" in out

    def test_history(self, capsys):
        """history выводит все команды или последние n."""
        em = Emulator4()
        for line in ("ls", "cd /", "who"):
            em.handle_line(line)
        assert em.handle_line(f"history {HISTORY_TAIL}")
        out = capsys.readouterr().out
        assert "who" in out and "history" in out
        assert "cd /" not in out

    def test_history_errors(self, capsys):
        """Неверный аргумент history."""
        assert not Emulator4().handle_line("history x")
        assert "numeric argument required" in capsys.readouterr().out

    def test_cal(self, capsys):
        """cal без аргументов, с годом, с месяцем и годом."""
        em = Emulator4()
        assert em.handle_line("cal")
        assert em.handle_line("cal 2 2024")
        assert em.handle_line("cal 2025")
        out = capsys.readouterr().out
        assert "February 2024" in out
        assert "29" in out
        assert "December" in out

    def test_cal_errors(self, capsys):
        """Неверные аргументы cal."""
        em = Emulator4()
        assert not em.handle_line("cal 13 2024")
        assert not em.handle_line("cal 1 x")
        assert not em.handle_line("cal 1 2 3")
        out = capsys.readouterr().out
        assert "invalid month" in out
        assert "invalid year" in out
        assert "too many arguments" in out

    def test_who(self, capsys):
        """who выводит пользователя, терминал и время входа."""
        em = Emulator4()
        assert em.handle_line("who")
        assert not em.handle_line("who x")
        out = capsys.readouterr().out
        assert em.username in out and "console" in out
        assert "extra operand" in out
