@echo off
rem Этап 3: загрузка разных вариантов VFS и ошибки загрузки.
setlocal
cd /d "%~dp0.."
for %%v in (vfs_minimal vfs_many vfs_deep vfs_invalid no_such_file) do (
    echo ===== %%v
    (echo conf-dump& echo exit) | python -m src.stage3 --vfs examples\%%v.csv --prompt "%%v> "
)
echo ===== startup script
python -m src.stage3 --vfs examples\vfs_deep.csv --script examples\startup_stage3.txt < nul
