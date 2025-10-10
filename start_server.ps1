# Library Management System Flask Backend Startup Script
Write-Host "Starting Library Management System Flask Backend..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Error: Python not found. Please install Python 3.7+ and try again." -ForegroundColor Red
    exit 1
}

# Check if requirements are installed
Write-Host "Checking requirements..." -ForegroundColor Yellow
try {
    python -c "import flask, flask_sqlalchemy, flask_cors" 2>$null
    Write-Host "Requirements are installed." -ForegroundColor Green
} catch {
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
python init_db.py

Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "The API will be available at: http://localhost:5002" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py
