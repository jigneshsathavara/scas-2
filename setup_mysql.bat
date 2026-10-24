@echo off
echo ========================================================
echo   Smart College Analytics System (SCAS) - Database Setup
echo ========================================================
echo.

echo Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not found in PATH!
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
pip install python-dotenv

echo.
echo Initializing MySQL database and seeding sample records...
python seed.py

echo.
echo ========================================================
echo   MySQL Database setup and seeding completed successfully!
echo ========================================================
pause
