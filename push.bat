@echo off
REM Quick push script for EXCELBOT
cd /d "%~dp0"
if "%1"=="" (
    echo Error: Please provide a commit message
    echo Usage: .\push.bat "Your commit message here"
    pause
    exit /b 1
)
"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "%*"
"C:\Program Files\Git\bin\git.exe" push origin main
echo.
echo Done! Railway will auto-deploy your changes.
pause

