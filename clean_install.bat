@echo off
echo Cleaning up and reinstalling dependencies...
echo.

echo Uninstalling potentially problematic packages...
pip uninstall -y faster-whisper av

echo.
echo Installing clean requirements...
pip install -r requirements.txt

echo.
echo Dependencies installed successfully!
echo You can now run: python run.py
pause
