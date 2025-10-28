# Test Backend Connection
Write-Host "Testing EduVerse Backend..." -ForegroundColor Cyan
Write-Host ""

# Test if backend is running
Write-Host "1. Testing backend health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -UseBasicParsing
    Write-Host "[OK] Backend is running!" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Backend is not running!" -ForegroundColor Red
    Write-Host "Please make sure the backend server is started." -ForegroundColor Yellow
    Write-Host "Run: .\quick_start.ps1" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "2. Testing registration endpoint..." -ForegroundColor Yellow

# Test registration with sample data
$testUser = @{
    username = "testuser_$(Get-Random -Maximum 9999)"
    email = "test_$(Get-Random -Maximum 9999)@example.com"
    password = "password123"
    full_name = "Test User"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/register" -Method POST -Body $testUser -ContentType "application/json" -UseBasicParsing
    Write-Host "[OK] Registration endpoint works!" -ForegroundColor Green
    Write-Host "Status Code: $($response.StatusCode)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Registration failed!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to get error details
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $reader.DiscardBufferedData()
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "3. Checking database connection..." -ForegroundColor Yellow

# Check if we can query the database
$backendPath = "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
$venvPython = "$backendPath\venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    $testScript = @"
import sys
sys.path.insert(0, '$($backendPath.Replace('\', '\\'))')
from database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM users'))
        count = result.scalar()
        print(f'[OK] Database connected. Users count: {count}')
except Exception as e:
    print(f'[ERROR] Database error: {e}')
"@
    
    $testScript | & $venvPython -
} else {
    Write-Host "[WARNING] Virtual environment not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Diagnostic Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan