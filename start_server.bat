@echo off
echo Starting Library Management System Flask Backend...
echo.
echo Make sure you have installed the requirements:
echo pip install -r requirements.txt
echo.
echo Initializing database...
python init_db.py
echo.
echo Starting Flask server...
echo The API will be available at: http://localhost:5002
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
