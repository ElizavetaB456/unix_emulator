@echo off
rem Этап 2: проверка всех параметров командной строки эмулятора.
setlocal
cd /d "%~dp0.."
call :run
call :run --vfs examples\vfs_many.csv
call :run --prompt "my-shell> "
call :run --script examples\startup_stage2.txt
call :run --vfs examples\vfs_many.csv --prompt "emu> " --script examples\startup_stage2.txt
call :run --script examples\no_such_script.txt
python -m src.stage2 --help
exit /b 0

:run
echo ===== %*
(echo conf-dump& echo exit) | python -m src.stage2 %*
echo exit code: %ERRORLEVEL%
exit /b 0
