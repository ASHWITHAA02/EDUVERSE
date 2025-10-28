# EduVerse Project Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting EduVerse Learning Platform  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Start Backend
Write-Host "`nStarting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend'; Write-Host 'Backend Server Starting...' -ForegroundColor Green; uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_frontend'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; npm run dev"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  EduVerse is starting up!             " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nBackend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C in each window to stop the servers" -ForegroundColor Yellow