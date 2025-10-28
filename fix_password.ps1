# Fix PostgreSQL Password Configuration
Write-Host "=== PostgreSQL Password Fix ===" -ForegroundColor Cyan
Write-Host ""

# Find PostgreSQL installation
$pgPath = $null
$versions = 18..12
foreach ($ver in $versions) {
    $testPath = "C:\Program Files\PostgreSQL\$ver\bin\psql.exe"
    if (Test-Path $testPath) {
        $pgPath = "C:\Program Files\PostgreSQL\$ver\bin"
        Write-Host "[OK] Found PostgreSQL $ver at: $pgPath" -ForegroundColor Green
        break
    }
}

if (-not $pgPath) {
    Write-Host "[ERROR] PostgreSQL not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Testing database connection..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Please enter your PostgreSQL 'postgres' user password:" -ForegroundColor Cyan
$password = Read-Host -AsSecureString
$plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Test connection
Write-Host ""
Write-Host "Testing connection..." -ForegroundColor Yellow
$env:PGPASSWORD = $plainPassword
$testResult = & "$pgPath\psql.exe" -U postgres -d postgres -c "SELECT 1;" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Password is correct!" -ForegroundColor Green
    
    # Update .env file
    $envPath = "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend\.env"
    $envContent = Get-Content $envPath -Raw
    $newDatabaseUrl = "DATABASE_URL=postgresql://postgres:$plainPassword@localhost:5432/eduverse"
    
    if ($envContent -match "DATABASE_URL=.*") {
        $envContent = $envContent -replace "DATABASE_URL=.*", $newDatabaseUrl
        Set-Content -Path $envPath -Value $envContent -NoNewline
        Write-Host "[OK] Updated .env file with correct password" -ForegroundColor Green
    }
    
    # Now create the database
    Write-Host ""
    Write-Host "Creating eduverse database..." -ForegroundColor Yellow
    
    # Check if database exists
    $dbCheck = & "$pgPath\psql.exe" -U postgres -d postgres -t -c "SELECT 1 FROM pg_database WHERE datname='eduverse';" 2>&1
    
    if ($dbCheck -match "1") {
        Write-Host "[WARNING] Database 'eduverse' already exists" -ForegroundColor Yellow
        $drop = Read-Host "Drop and recreate? (y/N)"
        if ($drop -eq 'y' -or $drop -eq 'Y') {
            Write-Host "Dropping database..." -ForegroundColor Yellow
            & "$pgPath\psql.exe" -U postgres -d postgres -c "DROP DATABASE eduverse;" 2>&1 | Out-Null
            Write-Host "Creating database..." -ForegroundColor Yellow
            & "$pgPath\psql.exe" -U postgres -d postgres -c "CREATE DATABASE eduverse;" 2>&1 | Out-Null
            Write-Host "[OK] Database recreated" -ForegroundColor Green
        }
    } else {
        & "$pgPath\psql.exe" -U postgres -d postgres -c "CREATE DATABASE eduverse;" 2>&1 | Out-Null
        Write-Host "[OK] Database created" -ForegroundColor Green
    }
    
    # Create tables and seed data
    Write-Host ""
    Write-Host "Creating tables and seeding data..." -ForegroundColor Yellow
    
    $backendPath = "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
    $venvPython = "$backendPath\venv\Scripts\python.exe"
    
    if (Test-Path $venvPython) {
        Write-Host "Running create_tables.py..." -ForegroundColor Cyan
        & $venvPython "$backendPath\create_tables.py"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Tables created successfully" -ForegroundColor Green
            
            Write-Host ""
            Write-Host "Running seed_data.py..." -ForegroundColor Cyan
            & $venvPython "$backendPath\seed_data.py"
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[OK] Sample data seeded successfully" -ForegroundColor Green
                Write-Host ""
                Write-Host "========================================" -ForegroundColor Green
                Write-Host "DATABASE SETUP COMPLETE!" -ForegroundColor Green
                Write-Host "========================================" -ForegroundColor Green
                Write-Host ""
                Write-Host "Next step: Run .\quick_start.ps1 to launch the application" -ForegroundColor Cyan
            } else {
                Write-Host "[ERROR] Failed to seed data" -ForegroundColor Red
            }
        } else {
            Write-Host "[ERROR] Failed to create tables" -ForegroundColor Red
        }
    } else {
        Write-Host "[ERROR] Virtual environment not found at: $venvPython" -ForegroundColor Red
        Write-Host "Please run setup_database.ps1 first" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "[ERROR] Password is incorrect!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please try again with the correct password." -ForegroundColor Yellow
    Write-Host "If you forgot your password, you may need to reset it using pgAdmin." -ForegroundColor Yellow
}

# Clear password from environment
$env:PGPASSWORD = $null