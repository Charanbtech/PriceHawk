@echo off
echo 🦅 Starting PriceHawk Application...
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running
    echo Please install Docker Desktop and make sure it's running
    pause
    exit /b 1
)

echo ✅ Docker is available

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found, copying from .env.example
    copy "backend\.env.example" ".env"
    echo.
    echo 📝 Please edit .env file with your configuration:
    echo    - MongoDB URI
    echo    - Email credentials
    echo    - Secret keys
    echo.
    echo Press any key to continue after editing .env...
    pause
)

echo 🏗️  Building and starting containers...
docker-compose up --build -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo 🎉 PriceHawk is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:5000/api
echo 🏥 Health Check: http://localhost:5000/health
echo.
echo 📊 To view logs:
echo    docker-compose logs -f
echo.
echo 🛑 To stop:
echo    docker-compose down
echo.

REM Try to open the frontend in browser
start http://localhost:3000

echo Press any key to exit...
pause