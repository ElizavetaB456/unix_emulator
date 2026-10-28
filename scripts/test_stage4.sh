#!/bin/sh
# Этап 4: стартовый скрипт со всеми режимами ls, cd, history, cal, who
# и интерактивная проверка ошибок.
cd "$(dirname "$0")/.." || exit 1
PY="${PYTHON:-python3}"
"$PY" -m src.stage4 --vfs examples/vfs_deep.csv \
    --script examples/startup_stage4.txt </dev/null
echo "exit code: $?"
echo "===== errors"
"$PY" -m src.stage4 --vfs examples/vfs_deep.csv --prompt "" <<'INPUT'
ls /missing
ls -z
cd /home/user/docs/notes.txt
cd / /var
history abc
cal 13 2026
cal 1 year
who am i
exit
INPUT
