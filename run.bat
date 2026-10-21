@echo off
rem Запуск эмулятора. По умолчанию используется этап 5.
setlocal
if "%STAGE%"=="" set "STAGE=5"
if not "%STAGE%"=="1" if not "%STAGE%"=="2" if not "%STAGE%"=="3" if not "%STAGE%"=="4" if not "%STAGE%"=="5" (
    echo STAGE must be a number from 1 to 5 1>&2
    exit /b 2
)
python -m src.stage%STAGE% %*
exit /b %ERRORLEVEL%
