@echo off
echo Installing Python requirements...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python first.
    pause
    exit /b 1
)

:: Install requirements if requirements.txt exists
if exist "requirements.txt" (
    echo Found requirements.txt, installing packages...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements. Check your internet connection or pip.
        pause
        exit /b 1
    )
    echo Requirements installed successfully!
) else (
    echo Warning: requirements.txt not found. Packages may need manual installation.
)

echo Starting accessibility checker web app...
python app.py
pause
