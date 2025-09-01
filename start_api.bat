@echo off
echo Starting ShelfAssistant API...
echo.
echo API will be available at: http://localhost:8000
echo Interactive docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
