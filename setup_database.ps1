# EduVerse Database Setup Script
# This script automatically sets up the PostgreSQL database for EduVerse

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduVerse Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Common PostgreSQL installation paths
$possiblePaths = @(
    "C:\Program Files\PostgreSQL\18\bin",
    "C:\Program Files\PostgreSQL\17\bin",
    "C:\Program Files\PostgreSQL\16\bin",
    "C:\Program Files\PostgreSQL\15\bin",
    "C:\Program Files\PostgreSQL\14\bin",
    "C:\Program Files\PostgreSQL\13\bin",
    "C:\Program Files\PostgreSQL\12\bin",
    "C:\Program Files (x86)\PostgreSQL\18\bin",
    "C:\Program Files (x86)\PostgreSQL\17\bin",
    "C:\Program Files (x86)\PostgreSQL\16\bin",
    "C:\Program Files (x86)\PostgreSQL\15\bin",
    "C:\Program Files (x86)\PostgreSQL\14\bin"
)

# Find PostgreSQL installation
$psqlPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path "$path\psql.exe") {
        $psqlPath = "$path\psql.exe"
        Write-Host "[OK] Found PostgreSQL at: $path" -ForegroundColor Green
        break
    }
}

if (-not $psqlPath) {
    Write-Host "[ERROR] PostgreSQL not found in common locations" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please enter the full path to your PostgreSQL bin folder:" -ForegroundColor Yellow
    Write-Host "Example: C:\Program Files\PostgreSQL\16\bin" -ForegroundColor Gray
    $customPath = Read-Host "Path"
    
    if (Test-Path "$customPath\psql.exe") {
        $psqlPath = "$customPath\psql.exe"
        Write-Host "[OK] Found PostgreSQL at custom path" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] psql.exe not found at that location" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install PostgreSQL from: https://www.postgresql.org/download/" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Database Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get PostgreSQL password
Write-Host "Enter your PostgreSQL 'postgres' user password:" -ForegroundColor Yellow
$pgPassword = Read-Host -AsSecureString
$pgPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($pgPassword)
)

Write-Host ""
Write-Host "Creating database 'eduverse'..." -ForegroundColor Cyan

# Set password environment variable for psql
$env:PGPASSWORD = $pgPasswordPlain

# Create database
$createDbCommand = "CREATE DATABASE eduverse;"
$checkDbCommand = "SELECT 1 FROM pg_database WHERE datname='eduverse';"

try {
    # Check if database already exists
    $result = & $psqlPath -U postgres -h localhost -t -c $checkDbCommand 2>&1
    
    if ($result -match "1") {
        Write-Host "[WARNING] Database 'eduverse' already exists" -ForegroundColor Yellow
        Write-Host ""
        $recreate = Read-Host "Do you want to drop and recreate it? (y/N)"
        
        if ($recreate -eq "y" -or $recreate -eq "Y") {
            Write-Host "Dropping existing database..." -ForegroundColor Yellow
            & $psqlPath -U postgres -h localhost -c "DROP DATABASE eduverse;" 2>&1 | Out-Null
            
            Write-Host "Creating new database..." -ForegroundColor Cyan
            & $psqlPath -U postgres -h localhost -c $createDbCommand 2>&1 | Out-Null
            Write-Host "[OK] Database recreated successfully" -ForegroundColor Green
        } else {
            Write-Host "[OK] Using existing database" -ForegroundColor Green
        }
    } else {
        # Create new database
        & $psqlPath -U postgres -h localhost -c $createDbCommand 2>&1 | Out-Null
        Write-Host "[OK] Database 'eduverse' created successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] Error creating database: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. PostgreSQL service not running" -ForegroundColor Gray
    Write-Host "2. Incorrect password" -ForegroundColor Gray
    Write-Host "3. User 'postgres' does not have permissions" -ForegroundColor Gray
    exit 1
}

# Clear password from environment
$env:PGPASSWORD = $null

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Backend Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Update .env file
$backendPath = "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
$envPath = "$backendPath\.env"
$envExamplePath = "$backendPath\.env.example"

if (-not (Test-Path $envPath)) {
    if (Test-Path $envExamplePath) {
        Write-Host "Creating .env file from template..." -ForegroundColor Cyan
        Copy-Item $envExamplePath $envPath
    } else {
        Write-Host "Creating new .env file..." -ForegroundColor Cyan
        $randomKey = Get-Random
        $envFileContent = @"
# Database Configuration
DATABASE_URL=postgresql://postgres:$pgPasswordPlain@localhost:5432/eduverse

# JWT Secret (generate a random string)
SECRET_KEY=your-super-secret-key-change-this-in-production-$randomKey

# JWT Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini API (Optional - for AI features)
GOOGLE_API_KEY=your-gemini-api-key-here

# Environment
ENVIRONMENT=development
"@
        $envFileContent | Out-File -FilePath $envPath -Encoding UTF8
    }
}

# Update DATABASE_URL in .env
Write-Host "Updating database connection string..." -ForegroundColor Cyan
$envContent = Get-Content $envPath -Raw
$envContent = $envContent -replace 'DATABASE_URL=.*', "DATABASE_URL=postgresql://postgres:$pgPasswordPlain@localhost:5432/eduverse"
$envContent | Out-File -FilePath $envPath -Encoding UTF8 -NoNewline

Write-Host "[OK] .env file configured" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Database Tables & Sample Data" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
$venvPath = "$backendPath\venv"
if (-not (Test-Path "$venvPath\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    Set-Location $backendPath
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Cyan
    & "$venvPath\Scripts\pip.exe" install -r requirements.txt --quiet
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Creating database tables..." -ForegroundColor Cyan
Set-Location $backendPath
$createTablesOutput = & "$venvPath\Scripts\python.exe" create_tables.py 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Database tables created successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Error creating tables:" -ForegroundColor Red
    Write-Host $createTablesOutput -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Seeding sample data (courses, lessons, quizzes, users)..." -ForegroundColor Cyan
$seedDataOutput = & "$venvPath\Scripts\python.exe" seed_data.py 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Sample data seeded successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Error seeding data:" -ForegroundColor Red
    Write-Host $seedDataOutput -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Database 'eduverse' is ready with:" -ForegroundColor Cyan
Write-Host "  - 13 database tables" -ForegroundColor White
Write-Host "  - 4 sample courses" -ForegroundColor White
Write-Host "  - 12+ lessons" -ForegroundColor White
Write-Host "  - 30+ quiz questions" -ForegroundColor White
Write-Host "  - 4 sample users" -ForegroundColor White
Write-Host "  - Achievement badges" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start the backend server:" -ForegroundColor White
Write-Host "   cd eduverse_backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "2. In a new terminal, start the frontend:" -ForegroundColor White
Write-Host "   cd eduverse_frontend" -ForegroundColor Gray
Write-Host "   npm install" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open http://localhost:5173 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "Sample Login:" -ForegroundColor Yellow
Write-Host "  Email: john@example.com" -ForegroundColor White
Write-Host "  Password: password123" -ForegroundColor White
Write-Host ""
Write-Host "Happy Learning!" -ForegroundColor Cyan