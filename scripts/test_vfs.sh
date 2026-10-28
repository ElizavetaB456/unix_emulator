#!/bin/sh
# Этап 3: загрузка разных вариантов VFS: минимальной, с несколькими
# файлами (в том числе двоичным в base64), с тремя и более уровнями
# вложенности, а также ошибки (некорректная и отсутствующая VFS).
cd "$(dirname "$0")/.." || exit 1
PY="${PYTHON:-python3}"
for vfs in vfs_minimal vfs_many vfs_deep vfs_invalid no_such_file; do
    echo "===== $vfs"
    printf 'conf-dump\nexit\n' | "$PY" -m src.stage3 \
        --vfs "examples/$vfs.csv" --prompt "$vfs> "
    echo "exit code: $?"
done
echo "===== startup script"
"$PY" -m src.stage3 --vfs examples/vfs_deep.csv \
    --script examples/startup_stage3.txt </dev/null
