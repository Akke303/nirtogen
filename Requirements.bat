@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    exit /b
)

REM Ensure pip is installed
python -m ensurepip --default-pip

REM Upgrade pip to the latest version
python -m pip install --upgrade pip

REM Install required packages
pip install requests colorama

REM Create the cache directory and file if they don't exist
mkdir "C:\NirtoGen V3"
echo. > "C:\NirtoGen V3\cache.txt"

echo All required packages have been installed.
pause