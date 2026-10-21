#!/bin/sh
set -eu
printf 'exit\n' | python -m src.stage3 --vfs examples/vfs_minimal.csv --prompt "mini> " --script examples/startup_stage3.sh
printf 'exit\n' | python -m src.stage3 --vfs examples/vfs_many.csv --prompt "many> " --script examples/startup_stage3.sh
printf 'exit\n' | python -m src.stage3 --vfs examples/vfs_deep.csv --prompt "deep> " --script examples/startup_stage3.sh
