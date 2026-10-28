#!/bin/sh
# Запуск всех демонстрационных скриптов по этапам.
cd "$(dirname "$0")" || exit 1
for script in test_stage1.sh test_config.sh test_vfs.sh \
              test_stage4.sh test_stage5.sh; do
    echo "########## $script"
    sh "$script"
done
