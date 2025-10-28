# Reset and Reseed Database Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduVerse Database Reset & Reseed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get PostgreSQL password
$dbPassword = Read-Host "Enter PostgreSQL password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "Step 1: Dropping existing database..." -ForegroundColor Yellow

# Drop and recreate database
$dropDbCommand = @"
DROP DATABASE IF EXISTS eduverse;
CREATE DATABASE eduverse;
"@

$env:PGPASSWORD = $plainPassword
echo $dropDbCommand | psql -U postgres -h localhost 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database dropped and recreated successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to drop/create database" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Creating tables..." -ForegroundColor Yellow

# Activate virtual environment and create tables
Set-Location "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
& ".\venv\Scripts\Activate.ps1"

python create_tables.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tables created successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create tables" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Seeding database with new content..." -ForegroundColor Yellow

python seed_data.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database seeded successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to seed database" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Database Reset Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "New Features Added:" -ForegroundColor Yellow
Write-Host "  ✅ 5 comprehensive Python lessons with rich content" -ForegroundColor White
Write-Host "  ✅ 8 quiz questions (instead of 2)" -ForegroundColor White
Write-Host "  ✅ Working YouTube video embeds" -ForegroundColor White
Write-Host "  ✅ AI Chatbot with lesson content access" -ForegroundColor White
Write-Host ""
Write-Host "You can now start the application with: .\quick_start.ps1" -ForegroundColor Cyan
Write-Host ""