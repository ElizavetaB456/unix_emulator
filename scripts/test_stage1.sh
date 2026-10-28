#!/bin/sh
# Этап 1: REPL в интерактивном режиме (ввод подаётся через stdin).
# Показаны раскрытие переменных окружения, заглушки ls и cd,
# ошибки (неизвестная команда, неверные аргументы, кавычки) и exit.
cd "$(dirname "$0")/.." || exit 1
PY="${PYTHON:-python3}"
"$PY" -m src.stage1 <<'INPUT'
ls -la $HOME
cd "$HOME/my docs"
ls ${USER} ${HOME}/docs
echo hello
exit 1 2
exit abc
ls "unclosed
exit
INPUT
echo "exit code: $?"
