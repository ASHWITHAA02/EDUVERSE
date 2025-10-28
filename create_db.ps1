# Simple script to create the eduverse database

$psqlPath = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$password = "sathish123"

Write-Host "Creating eduverse database..." -ForegroundColor Cyan

# Set password environment variable
$env:PGPASSWORD = $password

# Check if database exists
$checkDb = & $psqlPath -U postgres -h localhost -d postgres -t -c "SELECT 1 FROM pg_database WHERE datname='eduverse';" 2>&1

if ($checkDb -match "1") {
    Write-Host "[WARNING] Database 'eduverse' already exists" -ForegroundColor Yellow
    $recreate = Read-Host "Drop and recreate? (y/N)"
    
    if ($recreate -eq "y" -or $recreate -eq "Y") {
        Write-Host "Dropping database..." -ForegroundColor Yellow
        & $psqlPath -U postgres -h localhost -d postgres -c "DROP DATABASE eduverse;" 2>&1 | Out-Null
        
        Write-Host "Creating database..." -ForegroundColor Cyan
        & $psqlPath -U postgres -h localhost -d postgres -c "CREATE DATABASE eduverse;" 2>&1 | Out-Null
        Write-Host "[OK] Database recreated" -ForegroundColor Green
    } else {
        Write-Host "[OK] Using existing database" -ForegroundColor Green
    }
} else {
    & $psqlPath -U postgres -h localhost -d postgres -c "CREATE DATABASE eduverse;" 2>&1 | Out-Null
    Write-Host "[OK] Database 'eduverse' created" -ForegroundColor Green
}

# Clear password
$env:PGPASSWORD = $null

Write-Host ""
Write-Host "Now creating tables and seeding data..." -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
.\venv\Scripts\Activate.ps1

Write-Host "Creating database tables..." -ForegroundColor Cyan
python create_tables.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Tables created successfully" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Seeding sample data..." -ForegroundColor Cyan
    python seed_data.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Sample data seeded successfully" -ForegroundColor Green
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  Database Setup Complete!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next step: Run .\quick_start.ps1 to launch EduVerse" -ForegroundColor Cyan
    } else {
        Write-Host "[ERROR] Failed to seed data" -ForegroundColor Red
    }
} else {
    Write-Host "[ERROR] Failed to create tables" -ForegroundColor Red
}