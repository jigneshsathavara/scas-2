@echo off
echo ========================================================
echo   Starting Smart College Analytics System (SCAS)
echo ========================================================
echo.

:: Check if MySQL is running on port 3306
netstat -ano | findstr :3306 >nul
if %errorlevel% neq 0 (
    echo [INFO] MySQL is not detected on port 3306.
    if exist "C:\xampp\mysql\bin\mysqld.exe" (
        echo [INFO] Starting XAMPP MySQL server in background...
        start "" "C:\xampp\mysql\bin\mysqld.exe" --defaults-file="C:\xampp\mysql\bin\my.ini" --basedir="C:\xampp\mysql" --datadir="C:\xampp\mysql\data" --standalone
        timeout /t 3 /nobreak >nul
    ) else (
        echo [WARNING] Please ensure MySQL server is running before continuing!
    )
) else (
    echo [INFO] MySQL is already running on port 3306.
)

echo.
echo [INFO] Launching SCAS Application on http://127.0.0.1:5000 ...
echo [INFO] Press Ctrl+C in this terminal window to stop the server.
echo.

if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" app.py
) else if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" app.py
) else (
    python app.py
)
pause
