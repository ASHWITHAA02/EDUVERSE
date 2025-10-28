# Reset EduVerse Database
Write-Host "Resetting EduVerse Database..." -ForegroundColor Cyan

# Set PostgreSQL password
$env:PGPASSWORD = "sathish123"

# Drop and recreate database
Write-Host "`nDropping existing database..." -ForegroundColor Yellow
psql -U postgres -c "DROP DATABASE IF EXISTS eduverse;"

Write-Host "Creating new database..." -ForegroundColor Yellow
psql -U postgres -c "CREATE DATABASE eduverse;"

Write-Host "`nCreating tables..." -ForegroundColor Yellow
Set-Location "C:\Users\Ashwithaa SK\Desktop\EduVerse\eduverse_backend"
python create_tables.py

Write-Host "`nSeeding database with enhanced content..." -ForegroundColor Yellow
python seed_data.py

Write-Host "`nDatabase reset complete!" -ForegroundColor Green
Write-Host "`nNew Features:" -ForegroundColor Cyan
Write-Host "  - 5 comprehensive Python lessons (expanded from 3)" -ForegroundColor Green
Write-Host "  - Working YouTube video embeds" -ForegroundColor Green
Write-Host "  - 8 quiz questions with 4 options each (expanded from 2)" -ForegroundColor Green
Write-Host "  - AI chatbot with lesson content access" -ForegroundColor Green
Write-Host "  - Mark as complete functionality" -ForegroundColor Green
Write-Host "`nReady to run the application!" -ForegroundColor Cyan