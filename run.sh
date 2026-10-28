#!/bin/sh
# Запуск выбранного этапа эмулятора (по умолчанию этап 5):
#   STAGE=4 ./run.sh --vfs examples/vfs_deep.csv
set -eu
cd "$(dirname "$0")"
STAGE="${STAGE:-5}"
case "$STAGE" in
    1|2|3|4|5) ;;
    *) echo "STAGE должен быть числом от 1 до 5" >&2; exit 2 ;;
esac
exec "${PYTHON:-python3}" -m "src.stage${STAGE}" "$@"
