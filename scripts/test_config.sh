#!/bin/sh
# Этап 2: проверка всех параметров командной строки эмулятора.
cd "$(dirname "$0")/.." || exit 1
PY="${PYTHON:-python3}"
run() {
    echo "===== $*"
    printf 'conf-dump\nexit\n' | "$PY" -m src.stage2 "$@"
    echo "exit code: $?"
}
run
run --vfs examples/vfs_many.csv
run --prompt "my-shell> "
run --script examples/startup_stage2.txt
run --vfs examples/vfs_many.csv --prompt "emu> " \
    --script examples/startup_stage2.txt
run --script examples/no_such_script.txt
"$PY" -m src.stage2 --help
