# EduVerse Quick Start Script
# Run this after setup_database.ps1 completes successfully

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduVerse Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
$frontendPath = "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_frontend"

# Check if database is set up
if (-not (Test-Path "$backendPath\.env")) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "Please run setup_database.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/3] Starting Backend Server..." -ForegroundColor Cyan
Write-Host ""

# Start backend in a new window
$backendScript = @"
Set-Location '$backendPath'
.\venv\Scripts\Activate.ps1
Write-Host '========================================' -ForegroundColor Green
Write-Host '  Backend Server Starting...' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Green
Write-Host ''
Write-Host 'API Documentation: http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host ''
uvicorn main:app --reload --host 0.0.0.0 --port 8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

Write-Host "[OK] Backend server starting in new window..." -ForegroundColor Green
Write-Host "      API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""

# Wait a bit for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "[2/3] Installing Frontend Dependencies..." -ForegroundColor Cyan
Write-Host ""

Set-Location $frontendPath

# Check if node_modules exists
if (-not (Test-Path "$frontendPath\node_modules")) {
    Write-Host "Installing npm packages (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to install frontend dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] Frontend dependencies already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/3] Starting Frontend Server..." -ForegroundColor Cyan
Write-Host ""

# Start frontend in a new window
$frontendScript = @"
Set-Location '$frontendPath'
Write-Host '========================================' -ForegroundColor Green
Write-Host '  Frontend Server Starting...' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Green
Write-Host ''
Write-Host 'Application: http://localhost:5173' -ForegroundColor Cyan
Write-Host ''
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "[OK] Frontend server starting in new window..." -ForegroundColor Green
Write-Host "      Application: http://localhost:5173" -ForegroundColor Gray

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  EduVerse is Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Two new windows have opened:" -ForegroundColor Cyan
Write-Host "  1. Backend Server (Port 8000)" -ForegroundColor White
Write-Host "  2. Frontend Server (Port 5173)" -ForegroundColor White
Write-Host ""
Write-Host "Wait about 10 seconds, then open:" -ForegroundColor Yellow
Write-Host "  http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "Sample Login Credentials:" -ForegroundColor Cyan
Write-Host "  Email: john@example.com" -ForegroundColor White
Write-Host "  Password: password123" -ForegroundColor White
Write-Host ""
Write-Host "API Documentation:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop the servers:" -ForegroundColor Yellow
Write-Host "  Close the two PowerShell windows that opened" -ForegroundColor Gray
Write-Host "  Or press Ctrl+C in each window" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy Learning!" -ForegroundColor Cyan