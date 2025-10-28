#!/bin/bash

echo "🦅 Starting PriceHawk Application..."
echo

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker and Docker Compose"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "Please start Docker daemon"
    exit 1
fi

echo "✅ Docker is available"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found, copying from .env.example"
    cp "backend/.env.example" ".env"
    echo
    echo "📝 Please edit .env file with your configuration:"
    echo "   - MongoDB URI"
    echo "   - Email credentials"
    echo "   - Secret keys"
    echo
    read -p "Press Enter to continue after editing .env..."
fi

echo "🏗️  Building and starting containers..."
docker-compose up --build -d

echo
echo "⏳ Waiting for services to start..."
sleep 10

echo
echo "🎉 PriceHawk is starting up!"
echo
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000/api"
echo "🏥 Health Check: http://localhost:5000/health"
echo
echo "📊 To view logs:"
echo "   docker-compose logs -f"
echo
echo "🛑 To stop:"
echo "   docker-compose down"
echo

# Try to open the frontend in browser (Linux/Mac)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
fi