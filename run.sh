#!/bin/sh
# Запуск выбранного этапа эмулятора. По умолчанию используется этап 5.
set -eu
STAGE="${STAGE:-5}"
case "$STAGE" in
    1|2|3|4|5) ;;
    *) echo "STAGE должен быть числом от 1 до 5" >&2; exit 2 ;;
esac
exec python -m "src.stage${STAGE}" "$@"
