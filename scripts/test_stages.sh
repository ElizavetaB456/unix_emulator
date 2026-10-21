#!/bin/sh
set -eu
python -m src.stage1 <<'EOF'
ls -la
cd /home
exit
EOF
python -m src.stage2 --vfs examples/vfs_many.csv --prompt "stage2> " --script examples/startup_stage2.sh <<'EOF'
exit
EOF
python -m src.stage3 --vfs examples/vfs_many.csv --prompt "stage3> " --script examples/startup_stage3.sh <<'EOF'
exit
EOF
if python -m src.stage4 --vfs examples/vfs_deep.csv --prompt "stage4> " --script examples/startup_stage4.sh <<'EOF'
exit
EOF
then
    echo "Stage 4 script unexpectedly succeeded despite its final error test."
else
    echo "Stage 4 correctly stopped on the first command error."
fi
python -m src.stage5 --vfs examples/vfs_deep.csv --prompt "stage5> " --script examples/startup_stage5.sh <<'EOF'
exit
EOF
