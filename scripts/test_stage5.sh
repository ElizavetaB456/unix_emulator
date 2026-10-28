#!/bin/sh
# Этап 5: стартовый скрипт с mkdir и mv и интерактивная проверка
# ошибок. CSV-файл VFS при этом не изменяется.
cd "$(dirname "$0")/.." || exit 1
PY="${PYTHON:-python3}"
BEFORE=$(cksum < examples/vfs_deep.csv)
"$PY" -m src.stage5 --vfs examples/vfs_deep.csv \
    --script examples/startup_stage5.txt </dev/null
echo "exit code: $?"
echo "===== errors"
"$PY" -m src.stage5 --vfs examples/vfs_deep.csv --prompt "" <<'INPUT'
mkdir
mkdir /home
mkdir /none/dir
mkdir /home/user/docs/notes.txt/dir
mv
mv /home
mv /missing /tmp
mv /home /home/user
mv /var /home/user/docs/notes.txt
mv /var/log /none/log
exit
INPUT
if [ "$BEFORE" = "$(cksum < examples/vfs_deep.csv)" ]; then
    echo "vfs_deep.csv не изменён"
fi
