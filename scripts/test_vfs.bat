@echo off
setlocal
rem Проверка загрузки минимальной, обычной и глубоко вложенной VFS.
python -c "print('exit')" | python -m src.stage3 --vfs examples/vfs_minimal.csv --prompt "mini> " --script examples/startup_stage3.sh
if errorlevel 1 exit /b 1
python -c "print('exit')" | python -m src.stage3 --vfs examples/vfs_many.csv --prompt "many> " --script examples/startup_stage3.sh
if errorlevel 1 exit /b 1
python -c "print('exit')" | python -m src.stage3 --vfs examples/vfs_deep.csv --prompt "deep> " --script examples/startup_stage3.sh
if errorlevel 1 exit /b 1
echo VFS checks passed.
